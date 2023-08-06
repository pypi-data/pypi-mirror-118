# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.

import logging
import awsiot.greengrasscoreipc

from awsiot.greengrasscoreipc.model import (
    ConfigurationUpdateEvents,
    GetConfigurationRequest,
    SubscribeToConfigurationUpdateRequest,
    QOS
)

from threading import Condition

FEEDBACKLOOP_COMPONENT = "aws.greengrass.FeedbackLoop"
QOS_TYPE = QOS.AT_LEAST_ONCE
TIMEOUT = 10

feedbackloop_update_condition = Condition()


class IPCUtils:
    def __init__(self, ipc_client):
        self.ipc_client = ipc_client

    def get_feedbackloop_configuration(self):
        r"""
        Ipc client creates a request and activates the operation to get the configuration of
        the feedbackloop configuration.
        :return: A dictionary object of DefaultConfiguration from the recipe.
        """
        try:
            request = GetConfigurationRequest(component_name=FEEDBACKLOOP_COMPONENT)
            operation = self.ipc_client.new_get_configuration()
            operation.activate(request).result(TIMEOUT)
            result = operation.get_response().result(TIMEOUT)
            return result.value
        except Exception as e:
            logging.error(
                "Exception occured during fetching the Feedback Loop configuration: {}".format(e)
            )
            exit(1)

    def get_feedbackloop_config_updates(self):
        r"""
        Ipc client creates a request and activates the operation to subscribe to the configuration changes.
        """
        try:
            subsreq = SubscribeToConfigurationUpdateRequest(component_name=FEEDBACKLOOP_COMPONENT)

            subscribe_operation = self.ipc_client.new_subscribe_to_configuration_update(
                FeedbackLoopConfigUpdateHandler()
            )
            subscribe_operation.activate(subsreq).result(TIMEOUT)
            subscribe_operation.get_response().result(TIMEOUT)
        except Exception as e:
            logging.error(
                "Exception occured during fetching the configuration updates: {}".format(e)
            )
            exit(1)


class FeedbackLoopConfigUpdateHandler(
    awsiot.greengrasscoreipc.client.SubscribeToConfigurationUpdateStreamHandler
):
    r"""
    Custom handle of the subscribed configuration events(steam,error and close).
    Notifies feedbackloop_update_condition on a stream event.
    """

    def on_stream_event(self, event: ConfigurationUpdateEvents) -> None:
        logging.info(event.configuration_update_event)
        with feedbackloop_update_condition:
            feedbackloop_update_condition.notify()

    def on_stream_error(self, error: Exception) -> bool:
        logging.error("Error in config update subscriber - {0}".format(error))
        return False

    def on_stream_closed(self) -> None:
        logging.info("Config update subscription stream was closed")


