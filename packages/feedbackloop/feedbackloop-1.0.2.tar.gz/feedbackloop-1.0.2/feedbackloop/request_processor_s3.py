# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import logging
import uuid
from threading import Thread
from feedbackloop.model.filename import Filename
from feedbackloop.model.s3_key import S3Key
from feedbackloop.model.s3_location import S3Location
from feedbackloop.service.status_publisher import StatusMessageSuccess
from feedbackloop.service.status_publisher import StatusMessageSampleDropped
from feedbackloop.service.status_publisher import StatusMessageError

COUNTER_SAMPLE_NOT_USED = "SampleNotUsed"
COUNTER_PUBLISHED_SAMPLE_AND_PREDICTION = "SampleAndPredictionPublished"


class RequestProcessor(Thread):
    '''
        Responsible for handling the resource intensive aspects of feedback upload
        requests (S3 upload and model prediction publishing)
    '''
    def __init__(
        self,
        request_queue,
        metrics_publisher,
        status_publisher,
        model_input_uploader,
        model_prediction_publisher
    ):
        Thread.__init__(self)
        self._request_queue = request_queue
        self._metrics_publisher = metrics_publisher
        self._status_publisher = status_publisher
        self._model_input_uploader = model_input_uploader
        self._model_prediction_publisher = model_prediction_publisher

    def _handle(self, feedback_input, feedback_config):
        sampling_strategy = feedback_config.sampling_strategy

        if feedback_input.filename:
            filename = Filename(feedback_input.filename, feedback_config.file_ext)
        else:
            # If no filename argument is given to S3Key, a UUID will be used
            filename = Filename(str(uuid.uuid4()), feedback_config.file_ext)
        s3_key = S3Key(prefix=feedback_config.s3_prefix, filename=filename)
        model_input_upload_location = S3Location(feedback_config.s3_bucket, s3_key)
        if not sampling_strategy or sampling_strategy.should_use_sample(feedback_input.model_prediction):
            try:
                upload_result = self._model_input_uploader.upload(
                    s3_location=model_input_upload_location,
                    model_input=feedback_input.model_input,
                    content_type=feedback_config.content_type,
                    metadata=feedback_input.metadata
                )
            except Exception as e:
                error_str = "Failed to upload model input data due to exception. Model prediction will not be published. Exception type: {}, error: {}".format(
                 type(e).__name__, e
                )
                logging.warn(error_str)
                self._status_publisher.publish(StatusMessageError(exception=e, message=error_str), feedback_input.status_topic)
            else:
                self._model_prediction_publisher.publish(
                    config_id=feedback_input.config_id,
                    model_prediction=feedback_input.model_prediction,
                    model_input_location=model_input_upload_location,
                    metadata=feedback_input.metadata,
                    prediction_topic=feedback_input.prediction_topic
                )
                self._metrics_publisher.publish_counter(COUNTER_PUBLISHED_SAMPLE_AND_PREDICTION, 1)
                success_str = "Successfully uploaded model input and published model prediction."
                logging.info(success_str)
                self._status_publisher.publish(StatusMessageSuccess(s3_response_json=upload_result), feedback_input.status_topic)
        else:
            logging.info("Model input and model prediction were dropped by the configured sampling strategy for feedback configuration with id: {}".format(feedback_input.config_id))
            self._metrics_publisher.publish_counter(COUNTER_SAMPLE_NOT_USED, 1)
            self._status_publisher.publish(StatusMessageSampleDropped(), feedback_input.status_topic)

    def _process_input(self):
        # Queue::get will default to blocking if the queue is empty
        feedback_input, feedback_config = self._request_queue.get()
        try:
            logging.info("Processing request.")
            self._handle(feedback_input, feedback_config)
        except Exception as e:
            logging.warn(
                "Unexpected exception raised while processing request. Exception type: {}, error: {}".format(
               type(e).__name__, e
            ))
        finally:
            # call task done to indicate to queue that request
            # has been processed.
            logging.info("Finished processing request.")
            self._request_queue.task_done()

    def run(self):
        while True:
            self._process_input()
