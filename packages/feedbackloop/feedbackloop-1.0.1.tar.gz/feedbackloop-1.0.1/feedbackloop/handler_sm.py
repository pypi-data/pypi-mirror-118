# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import logging
from threading import Thread

try:
    import queue
except ImportError:
    import Queue as queue

import awsiot.greengrasscoreipc

from feedbackloop.stream_manager import (
    ExportDefinition,
    ResourceNotFoundException,
    MessageStreamDefinition,
    Persistence,
    S3ExportTaskExecutorConfig,
    Status,
    StatusConfig,
    StatusLevel,
    StatusMessage,
    StrategyOnFull,
    StreamManagerClient,
)

from feedbackloop.service.IPCUtils import IPCUtils, feedbackloop_update_condition
from feedbackloop.model.feedback_input import FeedbackInput, PARAM_CONFIG_ID, PARAM_MODEL_PREDICTION, \
                                              PARAM_METADATA, PARAM_STATUS_TOPIC, PARAM_PREDICTION_TOPIC, PARAM_FILENAME
from feedbackloop.model.component_config import (
    ComponentConfig, PARAM_FEEDBACK_CONFIG_MAP, PARAM_MAX_REQUESTS)
from feedbackloop.request_processor_sm import RequestProcessor
from feedbackloop.service.cloudwatch_metrics_publisher import CWComponentMetricsPublisher
from feedbackloop.service.model_input_uploader_sm import ModelInputUploaderSM
from feedbackloop.service.model_prediction_publisher import ModelPredictionPublisher, DEFAULT_PREDICTION_TOPIC
from feedbackloop.service.status_publisher import StatusPublisher, StatusMessageError, DEFAULT_STATUS_TOPIC

COUNTER_INVALID_COMPONENT_CONFIG = "ErrorInvalidComponentConfig"
COUNTER_INVALID_INPUT = "ErrorInvalidInput"
COUNTER_REQUEST_THROTTLED = "ErrorRequestThrottled"

ipc_client = awsiot.greengrasscoreipc.connect()
ipc_utils = IPCUtils(ipc_client)
model_prediction_publisher = ModelPredictionPublisher(ipc_client)
metrics_publisher = CWComponentMetricsPublisher(ipc_client)
status_publisher = StatusPublisher(ipc_client)

s3_client = StreamManagerClient()

model_input_uploader = ModelInputUploaderSM(s3_client, metrics_publisher)


def create_stream(stream_name=None, parameters=None):
    '''
        Create stream with name stream_name with the given parameters
        If stream already exists, warn user and return without doing anything.
    '''
    if not isinstance(stream_name, str):
        raise ValueError("stream_name argument must be of type string.")

    if not isinstance(parameters, dict):
        raise ValueError("parameters argument must be of type dict.")

    streams = s3_client.list_streams()
    if stream_name in streams:
        logging.warn("Stream with name [{}] already exists".format(stream_name))
        return

    status_stream_name = stream_name + "Status"

    exports = ExportDefinition(
        s3_task_executor=[
            S3ExportTaskExecutorConfig(
                identifier="S3TaskExecutor" + stream_name,  # Required
                # Optional. Add an export status stream to add statuses for all S3 upload tasks.
                status_config=StatusConfig(
                    status_level=StatusLevel.INFO,  # Default is INFO level statuses.
                    # Status Stream should be created before specifying in S3 Export Config.
                    status_stream_name=status_stream_name,
                ),
            )
        ]
    )

    DEFAULT_MAX_SIZE = 268435456
    DEFAULT_SEGMENT_SIZE = 16777216

    max_size = parameters.get("max_size") if parameters.get("max_size") else DEFAULT_MAX_SIZE
    stream_segment_size = parameters.get("stream_segment_size") if parameters.get("stream_segment_size") else DEFAULT_SEGMENT_SIZE
    time_to_live_millis = parameters.get("time_to_live_millis")

    strategy_on_full = parameters.get("strategy_on_full")
    if strategy_on_full == 0:
        strategy_on_full = StrategyOnFull.RejectNewData
    else:
        #default is OverwriteOldestData
        strategy_on_full = StrategyOnFull.OverwriteOldestData

    persistence = parameters.get("persistence")
    if persistence == 1:
        persistence = Persistence.Memory
    else:
        #default is File
        persistence = Persistence.File
    flush_on_write = parameters.get("flush_on_write")

    # Create the Status Stream with default parameters
    s3_client.create_message_stream(
        MessageStreamDefinition(name=status_stream_name, strategy_on_full=StrategyOnFull.OverwriteOldestData)
    )

    # Create the message stream with the S3 Export definition and given parameters.
    s3_client.create_message_stream(
        MessageStreamDefinition(
            name=stream_name,
            max_size=max_size,
            stream_segment_size=stream_segment_size,
            time_to_live_millis=time_to_live_millis,
            strategy_on_full=strategy_on_full,
            persistence=persistence,
            flush_on_write=flush_on_write,
            export_definition=exports
        )
    )


def update_stream(stream_name, parameters):
    '''
        Update stream with name stream_name with the given parameters
        If no such stream exists, raise ValueError
    '''
    if not isinstance(stream_name, str):
        raise ValueError("stream_name argument must be of type string.")

    if not isinstance(parameters, dict):
        raise ValueError("parameters argument must be of type dict.")

    streams = s3_client.list_streams()
    if stream_name in streams:
        status_stream_name = stream_name + "Status"

        exports = ExportDefinition(
            s3_task_executor=[
                S3ExportTaskExecutorConfig(
                    identifier="S3TaskExecutor" + stream_name,  # Required
                    # Optional. Add an export status stream to add statuses for all S3 upload tasks.
                    status_config=StatusConfig(
                        status_level=StatusLevel.INFO,  # Default is INFO level statuses.
                        # Status Stream should be created before specifying in S3 Export Config.
                        status_stream_name=status_stream_name,
                    ),
                )
            ]
        )

        DEFAULT_MAX_SIZE = 268435456
        DEFAULT_SEGMENT_SIZE = 16777216

        max_size = parameters.get("max_size") if parameters.get("max_size") else DEFAULT_MAX_SIZE
        stream_segment_size = parameters.get("stream_segment_size") if parameters.get(
            "stream_segment_size") else DEFAULT_SEGMENT_SIZE
        time_to_live_millis = parameters.get("time_to_live_millis")

        strategy_on_full = parameters.get("strategy_on_full")
        if strategy_on_full == 0:
            strategy_on_full = StrategyOnFull.RejectNewData
        else:
            # default is OverwriteOldestData
            strategy_on_full = StrategyOnFull.OverwriteOldestData

        persistence = parameters.get("persistence")
        if persistence == 1:
            persistence = Persistence.Memory
        else:
            # default is File
            persistence = Persistence.File
        flush_on_write = parameters.get("flush_on_write")

        # Create the message stream with the S3 Export definition and given parameters.
        s3_client.update_message_stream(
            MessageStreamDefinition(
                name=stream_name,
                max_size=max_size,
                stream_segment_size=stream_segment_size,
                time_to_live_millis=time_to_live_millis,
                strategy_on_full=strategy_on_full,
                persistence=persistence,
                flush_on_write=flush_on_write,
                export_definition=exports
            )
        )
    else:
        logging.warn("Stream with name [{}] does not exist exists".format(stream_name))


def delete_stream(stream_name):
    '''
        Deletes a stream with name stream_name.
        If no stream with name stream_name, pass.
    '''
    if not isinstance(stream_name, str):
        raise ValueError("stream_name argument must be of type string.")

    # Try deleting the stream (if it exists)
    try:
        s3_client.delete_message_stream(stream_name=stream_name)
    except ResourceNotFoundException:
        pass

    status_stream_name = stream_name + "Status"
    try:
        s3_client.delete_message_stream(stream_name=status_stream_name)
    except ResourceNotFoundException:
        pass


def modify_configuration(new_configuration):
    try:
        # This try block is for catching user configuration errors
        new_component_param_feedback_config = new_configuration.get(PARAM_FEEDBACK_CONFIG_MAP)
        new_component_param_max_requests = new_configuration.get(PARAM_MAX_REQUESTS)
        new_component_config = ComponentConfig(
            int(new_component_param_max_requests if new_component_param_feedback_config else 0),
            new_component_param_feedback_config
        )
        return new_component_config
    except Exception as e:
        metrics_publisher.publish_counter(COUNTER_INVALID_COMPONENT_CONFIG, 1)
        error_str = "Failed to initialize. Exception raised while parsing component configuration. Stopping component execution. Failed with: {}".format(
            e)
        logging.error(error_str)
        raise e


# Listen to see if feedback configuration map changes, if so, update the current component configuration
def wait_for_config_changes():
    with feedbackloop_update_condition:
        feedbackloop_update_condition.wait()
        global component_config
        component_config = modify_configuration(ipc_utils.get_feedbackloop_configuration())
    wait_for_config_changes()


# initialize component config
component_config = modify_configuration(ipc_utils.get_feedbackloop_configuration())

try:
    # This try block is for catching unexpected errors
    request_queue = queue.Queue(component_config.max_requests)
    request_processor = RequestProcessor(
        request_queue=request_queue,
        metrics_publisher=metrics_publisher,
        status_publisher=status_publisher,
        model_input_uploader=model_input_uploader,
        model_prediction_publisher=model_prediction_publisher
    )

    # request_processor runs on a separate thread and listens for
    # events published to the request_queue.
    request_processor.start()
except Exception as e:
    error_str = "Failed to initialize. Unexpected exception raised:{}".format(e)
    logging.error(error_str)
    raise e

logging.info("Successfully initialized the feedback component.")
# Subscribe to the subsequent configuration changes
ipc_utils.get_feedbackloop_config_updates()

Thread(
    target=wait_for_config_changes,
    args=(),
).start()


def handle_error(exception, error_str, counter, topic):
    metrics_publisher.publish_counter(counter, 1)
    logging.warn(error_str)
    error_message = StatusMessageError(exception=exception, message=error_str)
    status_publisher.publish(error_message, topic)


def function_handler(model_input, handler_data, stream_name):
    # Validate input and return to client immediately if something is
    # wrong.
    status_topic = handler_data.get(PARAM_STATUS_TOPIC)

    try:
        feedback_input = FeedbackInput(model_input, handler_data)
        if feedback_input.config_id not in component_config.feedback_config_map:
            raise ValueError("Feedback configuration map does not contain config_id: {}".format(feedback_input.config_id))
        feedback_config = component_config.feedback_config_map[feedback_input.config_id]
    except Exception as e:
        error_str = "Exception raised while parsing input. Failed with exception type: {}, error: {}".format(type(e).__name__, e)
        handle_error(exception=e, error_str=error_str, counter=COUNTER_INVALID_INPUT, topic=status_topic)
        raise e

    try:
        logging.info("Enqueing request to be processed.")
        request_queue.put_nowait((feedback_input, feedback_config, stream_name))
    except queue.Full as e:
        error_str = "Request limit has been reached (max request:{}). Dropping request.".format(component_config.max_requests)
        handle_error(exception=e, error_str=error_str, counter=COUNTER_REQUEST_THROTTLED, topic=status_topic)
        raise e

    logging.info("Request has successfully be enqueued.")
    return


def publish(model_input,
            model_prediction,
            config_id,
            stream_name,
            filename=None,
            prediction_topic=None,
            status_topic=None,
            metadata=None):
    """
    Customer facing function that is responsible for packaging feedback input data
    (e.g. config id, model prediction, etc.) and model input (ex: inference images)
    together in format readable by the feedback loop handler
    """
    prediction_topic = prediction_topic if prediction_topic else DEFAULT_PREDICTION_TOPIC
    status_topic = status_topic if status_topic else DEFAULT_STATUS_TOPIC

    feedback_input_data = {
        PARAM_CONFIG_ID: config_id,
        PARAM_MODEL_PREDICTION: model_prediction,
        PARAM_METADATA: metadata,
        PARAM_FILENAME: filename,
        PARAM_PREDICTION_TOPIC: prediction_topic,
        PARAM_STATUS_TOPIC: status_topic
    }

    # pass model input and handler_data onto data handler
    function_handler(
        model_input=model_input,
        handler_data=feedback_input_data,
        stream_name=stream_name
    )