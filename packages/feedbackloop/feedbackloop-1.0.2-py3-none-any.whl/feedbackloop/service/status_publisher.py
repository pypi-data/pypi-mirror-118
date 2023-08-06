# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import json
import logging
import feedbackloop.service.status_messages as StatusResponse
from abc import ABCMeta, abstractmethod

from awsiot.greengrasscoreipc.model import (
    PublishToIoTCoreRequest
)

from feedbackloop.service.IPCUtils import QOS_TYPE, TIMEOUT

FIELD_S3_RESPONSE = "s3_response"
VALUE_SAMPLE_DROPPED = "sample_dropped_by_strategy"

DEFAULT_STATUS_TOPIC = "feedback/message/status"

class StatusMessage(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def payload(self):
        pass


class StatusMessageSuccess(StatusMessage):
    def __init__(self, s3_response_json):
        response_fields = {
            FIELD_S3_RESPONSE : s3_response_json
        }
        self._response = StatusResponse.generate_success_response(**response_fields)

    @property
    def payload(self):
        return json.dumps(self._response)


class StatusMessageSampleDropped(StatusMessage):
    def __init__(self):
        success_message = StatusResponse.generate_success_response()
        success_message[StatusResponse.RESPONSE_FIELD_STATUS] = VALUE_SAMPLE_DROPPED
        self._response = success_message

    @property
    def payload(self):
        return json.dumps(self._response)


class StatusMessageError(StatusMessage):
    def __init__(self, exception, message):
        if not isinstance(exception, Exception):
            raise ValueError("StatusMessageError requires exception to be of type Exception.")
        self._response = StatusResponse.generate_error_response(type(exception).__name__, message)

    @property
    def payload(self):
        return json.dumps(self._response)


class StatusPublisher(object):
    def __init__(self, iot_client):
        self._client = iot_client

    def publish(self, status_message, status_topic):
        if not isinstance(status_message, StatusMessage):
            raise ValueError("status_message must be of type StatusMessage.")

        logging.info("Publishing status message to topic: {}, with message payload: {}".format(
            status_topic, str(status_message.payload)
        ))

        request = PublishToIoTCoreRequest()
        request.topic_name = status_topic
        request.qos = QOS_TYPE

        request.payload = bytes(status_message.payload, "utf-8")

        operation = self._client.new_publish_to_iot_core()
        operation.activate(request)
        future = operation.get_response()
        future.result(TIMEOUT)
