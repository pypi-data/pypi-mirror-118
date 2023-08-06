# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.

from feedbackloop.model.config_id import ConfigId
PARAM_CONFIG_ID = "ConfigId"
PARAM_MODEL_PREDICTION = "ModelPrediction"
PARAM_METADATA = "Metadata"
PARAM_CONFIG_ID = "FeedbackConfigID"
PARAM_PREDICTION_TOPIC = "PublishPredictionsOnTopic"
PARAM_STATUS_TOPIC = "PublishStatusOnTopic"
PARAM_FILENAME = "Filename"


class FeedbackInput (object):
    '''
        Responsible for validating and storing IPC requests
        to the feedback component.
    '''

    def __init__(self, model_input, context):
        if PARAM_CONFIG_ID not in context:
            raise ValueError("Failed to construct FeedbackInput. Context is missing param: {}".format(PARAM_CONFIG_ID))
        self._config_id = ConfigId(context[PARAM_CONFIG_ID])

        if PARAM_MODEL_PREDICTION not in context:
            raise ValueError("Failed to construct FeedbackInput. Context is missing param: {}".format(PARAM_MODEL_PREDICTION))
        model_prediction = context[PARAM_MODEL_PREDICTION]
        # The model prediction of Image classification is a list, and that if Object Detection is a dict
        if not isinstance(model_prediction, list) and not isinstance(model_prediction, dict):
            raise ValueError("Failed to construct FeedbackInput. ModelPrediction param must be a list or a dict.")
        if not model_prediction:
            raise ValueError("Failed to construct FeedbackInput. ModelPrediction param cannot be empty.")
        self._model_prediction = model_prediction

        self._metadata = context.get(PARAM_METADATA)
        if self._metadata:
            if not isinstance(self._metadata, dict):
                raise ValueError("Failed to construct FeedbackInput. Metadata param must be a dict.")
        else:
            self._metadata = {}

        self._prediction_topic = context.get(PARAM_PREDICTION_TOPIC)
        self._status_topic = context.get(PARAM_STATUS_TOPIC)

        self._filename = context.get(PARAM_FILENAME)

        self._model_input = model_input

    @property
    def config_id(self):
        return self._config_id.id

    @property
    def model_prediction(self):
        return self._model_prediction

    @property
    def metadata(self):
        return self._metadata

    @property
    def prediction_topic(self):
        return self._prediction_topic

    @property
    def filename(self):
        return self._filename

    @property
    def status_topic(self):
        return self._status_topic

    @property
    def model_input(self):
        return self._model_input
