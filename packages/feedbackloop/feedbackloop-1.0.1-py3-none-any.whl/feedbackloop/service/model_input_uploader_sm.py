# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import logging
import sys
import time

from feedbackloop.stream_manager import (
    ReadMessagesOptions,
    S3ExportTaskDefinition,
    Status,
    StatusMessage,
    StreamManagerException,
)
from feedbackloop.stream_manager.util import Util

COUNTER_UPLOAD_OBJECT_SUCCESS = "SampleUploadSuccess"
COUNTER_UPLOAD_OBJECT_FAILURE = "SampleUploadFailure"
BYTES_SAMPLE_SIZE = "SampleSize"

RESPONSE_KEY_S3_BUCKET = "bucket"
RESPONSE_KEY_S3_KEY = "key"

FILE_URI_PREFIX = "file:"


class ModelInputUploaderSM(object):
    '''
        Responsible for uploading the input of ML models
        to S3. Ex. image, sound clip, etc
    '''
    def __init__(self, sm_client, cw_metrics_publisher):
        self._client = sm_client
        self._metrics_publisher = cw_metrics_publisher

    def upload(self, s3_location, model_input, content_type, stream_name, metadata):
        # Publish size of payload on every request. This may provide
        # a useful hint in case of upload failures.
        payload = open(model_input, 'rb').read()

        self._metrics_publisher.publish_bytes(BYTES_SAMPLE_SIZE, sys.getsizeof(payload))

        # Append a S3 Task definition and print the sequence number
        try:
            file_uri = FILE_URI_PREFIX + model_input
            s3_export_task_definition = S3ExportTaskDefinition(input_url=file_uri,
                                                               bucket=s3_location.bucket,
                                                               key=s3_location.key.key,
                                                               user_metadata=metadata if metadata else {})
            logging.info(
                "Successfully appended S3 Task Definition to stream with sequence number %d",
                self._client.append_message(stream_name, Util.validate_and_serialize_to_json_bytes(s3_export_task_definition)),
            )
        except Exception as e:
            logging.info("Failed to append S3 Task Definition")

        # Read the statuses from the export status stream
        stop_checking = False
        next_seq = 0
        response = {
            "bucket": s3_location.bucket,
            "key": s3_location.key.key
        }

        while not stop_checking:
            try:
                status_stream_name = stream_name + "Status"
                messages_list = self._client.read_messages(
                    status_stream_name,
                    ReadMessagesOptions(
                        desired_start_sequence_number=next_seq, min_message_count=1, read_timeout_millis=1000
                    ),
                )
                for message in messages_list:
                    # Deserialize the status message first.
                    status_message = Util.deserialize_json_bytes_to_obj(message.payload, StatusMessage)

                    # Check the status of the status message. If the status is "Success",
                    # the file was successfully uploaded to S3.
                    # If the status was either "Failure" or "Cancelled", the server was unable to upload the file to S3.
                    # If the status was "InProgress", this indicates that the server has started uploading the S3 task.
                    if status_message.status == Status.Success:
                        # Add extra fields to the response
                        logging.info("Successfully uploaded model input {} to S3 location: {}.".format(model_input, str(s3_location.uri)))
                        self._metrics_publisher.publish_counter(COUNTER_UPLOAD_OBJECT_SUCCESS, 1)
                        stop_checking = True
                    elif status_message.status == Status.InProgress:
                        logging.info("File upload is in Progress.")
                        next_seq = message.sequence_number + 1
                    elif status_message.status == Status.Failure or status_message.status == Status.Canceled:
                        logging.warn("Failed to upload object to S3 location: {}, with exception type: {}, error: {}.".format(str(s3_location.uri), type(e).__name__, e))
                        self._metrics_publisher.publish_counter(COUNTER_UPLOAD_OBJECT_FAILURE, 1)
                        stop_checking = True
                if not stop_checking:
                    time.sleep(5)
            except StreamManagerException:
                logging.exception("Exception while running")
                time.sleep(5)

        return response


