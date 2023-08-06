# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
import json
import logging
from datetime import datetime

from awsiot.greengrasscoreipc.model import (
    PublishToIoTCoreRequest
)

from feedbackloop.service.IPCUtils import QOS_TYPE, TIMEOUT

DEFAULT_PREDICTION_TOPIC = "feedback/message/prediction"

class ModelPredictionPublisher(object):
    def __init__(self, ipc_client):
        self._client = ipc_client

    def publish(self, config_id, model_prediction, model_input_location, metadata, prediction_topic, timestamp=datetime.now()):
        '''
        Publishes prediction to IoT Core topic prediction_topic through MQTT.
        Also logs timestamp of prediction upload in metadata.
        '''
        request = PublishToIoTCoreRequest()
        request.topic_name = prediction_topic
        request.qos = QOS_TYPE

        extra_metadata = {}

        if timestamp:
            extra_metadata["publish-ts"] = str(timestamp)

        metadata.update(extra_metadata)

        request.payload = bytes(json.dumps({
                "source-ref": model_input_location.uri,
                "model-prediction": model_prediction,
                "metadata": metadata,
                "config-id": config_id
            }), "utf-8")

        operation = self._client.new_publish_to_iot_core()
        operation.activate(request)
        future = operation.get_response()
        future.result(TIMEOUT)

        logging.info("Published model prediction for S3 object: {}, to MQTT topic: {} for feedback config-id: {}".format(
            model_input_location.uri, prediction_topic, config_id
        ))
