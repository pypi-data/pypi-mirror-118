# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
RESPONSE = "response"
RESPONSE_FIELD_STATUS = "status"
RESPONSE_FIELD_ERROR_MSG = "error_message"
RESPONSE_FIELD_ERROR_CLASS = "error"

VALUE_SUCCESS = "success"
VALUE_FAIL = "fail"


def generate_success_response(**kwargs):
 success_response = {
     RESPONSE: {
         RESPONSE_FIELD_STATUS: VALUE_SUCCESS
     }
 }

 if kwargs:
     success_response[RESPONSE].update(kwargs)

 return success_response


def generate_error_response(error_class, error_msg, **kwargs):
 error_response = {
     RESPONSE: {
         RESPONSE_FIELD_STATUS: VALUE_FAIL,
         RESPONSE_FIELD_ERROR_MSG: error_msg,
         RESPONSE_FIELD_ERROR_CLASS: error_class
     }
 }

 if kwargs:
     error_response[RESPONSE].update(kwargs)

 return error_response
