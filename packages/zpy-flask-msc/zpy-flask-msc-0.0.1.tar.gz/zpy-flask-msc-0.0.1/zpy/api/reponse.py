from zpy.utils import get_operation_id
from enum import Enum
from typing import Any
import json


__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


PAYLOAD_KEY: str = "data"
STATUS_KEY: str = "status"
DESCRIPTION_KEY: str = "description"
OPERATION_ID_KEY: str = "operationId"
ERRORS_KEY: str = "errors"


class Status(Enum):
    """
    Common HTTP status codes

    CODE | SHORT DESCRIPTION | STATUS DETAILS
    """

    SUCCESS                = (200, "SUCCEEDED", "The request has succeeded")
    CREATED                = (201, "CREATED","The request has been fulfilled and resulted in a new resource being created.")
    ACCEPTED               = (202, "ACCEPTED","The request has been accepted for processing, but the processing has not been completed.")
    NO_CONTENT             = (204, "NO CONTENT","The request has been completed successfully but your response has no content, although the headers can be useful.",)
    PARTIAL_CONTENT        = (206, "PARTIAL CONTENT", "Partial content")

    BAD_REQUEST            = (400, "BAD REQUEST","The request could not be understood by the server due to malformed syntax. The client SHOULD NOT repeat the request without modifications.",)
    UNAUTHORIZED           = (401, "UNAUTHORIZED", "The request requires user authentication.")
    FORBIDDEN              = (403, "FORBIDDEN","The server understood the request, but is refusing to fulfill it.")
    NOT_FOUND              = (404, "NOT FOUND","The server has not found anything matching the Request-URI.",)
    METHOD_NOT_ALLOWED     = (405, "METHOD NOT ALLOWED","The method specified in the Request-Line is not allowed for the resource identified by the Request-URI.",)
    CONTENT_NOT_ACCEPTABLE = (406, "METHOD NOT ACCEPTABLE","The resource identified by the request is only capable of generating response entities which have content characteristics not acceptable according to the accept headers sent in the request.",)
    REQUEST_TIMEOUT        = (408, "REQUEST TIMEOUT", "Time out")
    PRE_CONDITION_FAILED   = (412, "PRECONDITION FAILED","The client has indicated preconditions in their headers which the server does not meet.",)
    UNSUPPORTED_MEDIA_TYPE = (415, "UNSUPPORTED MEDIA TYPE","The multimedia format of the requested data is not supported by the server, therefore the server rejects the request.",)
    IM_A_TEAPOT            = (418, "IM A TEAPOT","The server refuses to try to make coffee with a kettle.",)
    CONFLICT               = (409, "CONFLICT", "The server found conflict with request supplied.")
    UNPROCESSABLE          = (422, "UNPROCESSABLE ENTITY","The process could not be completed due to a semantics error.",)
    LOCKED                 = (423, "LOCKED","The source or destination resource of a method is locked.",)

    INTERNAL_SERVER_ERROR  = (500, "INTERNAL SERVER ERROR","The server encountered an unexpected condition which prevented it from fulfilling the request.",)
    NOT_IMPEMENTED         = (501, "NOT IMPLEMENTED","The server does not support the functionality required to fulfill the request",)
    SERVICE_UNAVAIBLE      = (503, "SERVICE UNAVAIBLE","The server is currently unable to handle the request due to a temporary overloading or maintenance of the server.",)
    GATEWAY_TIMEOUT        = (503, "GATEWAY TIMEOUT", "Timeout")
    LOOP_DETECTED          = (508, "LOOP DETECTED","The server encountered an infinite loop while processing the request. ",)


class Error:
    pass


class Builder:
    """
    Common resopnse builder
    """

    response = {
        PAYLOAD_KEY: {},
        DESCRIPTION_KEY: Status.SUCCESS.value[2],
        STATUS_KEY: Status.SUCCESS.value[1],
        OPERATION_ID_KEY: None,
    }
    response_code = 200

    def __init__(self, custom_schema=None) -> None:
        if custom_schema is not None:
            self.response = custom_schema

    def add_custom(self, key: str, data: Any):
        """Add custom item to object body.

        PD: Replacemnt item if response body have a item

        Parameters
        ----------
        key : str | required
            The item key

        data : Any | required
            The item value

        Raises
        ------
        NotValueProvided
            If no values is set for the response or passed in as a
            parameter.
        """
        self.response[key] = data
        return self

    def add_error(self, error: any):
        """Add error to erros object body.

        PD: Replacemnt item if response body have a item

        Parameters
        ----------
        error : Any, str, dict | required
            The item error response

        Raises
        ------
        NotErrorProvided
            If no status is set for the response or passed in as a
            parameter.
        """
        if ERRORS_KEY in self.response:
            self.response[ERRORS_KEY].append(error)
        else:
            self.response[ERRORS_KEY] = [error]
        return self

    def add_payload(self, payload):
        """Add data payload to reponse body.

        PD: Replacemnt item if response body have a item

        Parameters
        ----------
        payload : Any, str, dict | required
            The data response

        Raises
        ------
        NotPayloadProvided
            If no status is set for the response or passed in as a
            parameter.
        """
        self.response[PAYLOAD_KEY] = payload
        return self

    def add_description(self, description: str):
        """Add description to reponse body.

        PD: Replacemnt if response body have a description

        Parameters
        ----------
        description : str | required
            The description response

        Raises
        ------
        NotDescriptionProvided
            If no status is set for the response or passed in as a
            parameter.
        """
        self.response[DESCRIPTION_KEY] = description
        return self

    def add_operation_id(self, id: str):
        """Add operation to reponse body.

        PD: Replacemnt if response body have a item

        Parameters
        ----------
        id : str | required
            The operation id response

        Raises
        ------
        NotValueProvided
            If no status is set for the response or passed in as a
            parameter.
        """
        self.response[OPERATION_ID_KEY] = id
        return self

    def add_status(self, status: Status):
        """Add status to reponse body.

        The status value is a tuple conformed by 3 parts:

        CODE | SHORT DESCRIPTION | STATUS DETAILS

        Parameters
        ----------
        status : Status | Tuple, required
            The response information

        Raises
        ------
        NotStatusProvided
            If no status is set for the response or passed in as a
            parameter.
        """
        self.response[STATUS_KEY] = status.value[1]
        self.response_code = status.value[0]
        self.response[DESCRIPTION_KEY] = status.value[2]
        return self

    @staticmethod
    def success(
        payload={},
        status_code: Status = Status.SUCCESS,
        operation_id=None,
        description: str = None,
        fn_transform = None
    ):
        response = {}
        response[OPERATION_ID_KEY] = (
            get_operation_id() if operation_id is None else operation_id
        )
        response[PAYLOAD_KEY] = payload
        response[DESCRIPTION_KEY] = (
            status_code.value[2] if description is None else description
        )
        response[STATUS_KEY] = status_code.value[1]
        if fn_transform != None:
            response = fn_transform(response)
        return response, status_code.value[0]

    @staticmethod
    def error(
        payload={},
        errors=[],
        status=Status.INTERNAL_SERVER_ERROR,
        operation_id=None,
        description: str = None,
        fn_transform=None,
    ):
        response = {}
        response[OPERATION_ID_KEY] = (
            get_operation_id() if operation_id is None else operation_id
        )
        response[ERRORS_KEY] = errors
        response[PAYLOAD_KEY] = payload
        response[DESCRIPTION_KEY] = (
            status.value[2] if description is None else description
        )
        response[STATUS_KEY] = status.value[1]

        if fn_transform != None:
            response = fn_transform(response)

        return response, status.value[0]

    @staticmethod
    def bad_request(
        payload={},
        errors=[],
        status=Status.BAD_REQUEST,
        operation_id=None,
        description: str = None,
        fn_transform=None,
    ):
        response = {}
        response[OPERATION_ID_KEY] = (
            get_operation_id() if operation_id is None else operation_id
        )
        response[ERRORS_KEY] = errors
        response[PAYLOAD_KEY] = payload
        response[DESCRIPTION_KEY] = (
            status.value[2] if description is None else description
        )
        response[STATUS_KEY] = status.value[1]
        if fn_transform != None:
            response = fn_transform(response)
        return response, status.value[0]

    @staticmethod
    def no_content(
        payload={},
        errors=[],
        status=Status.NO_CONTENT,
        operation_id=None,
        description: str = None,
        fn_transform=None,
    ):
        response = {}
        response[OPERATION_ID_KEY] = (
            get_operation_id() if operation_id is None else operation_id
        )
        response[ERRORS_KEY] = errors
        response[PAYLOAD_KEY] = payload
        response[DESCRIPTION_KEY] = (
            status.value[2] if description is None else description
        )
        response[STATUS_KEY] = status.value[1]
        if fn_transform != None:
            response = fn_transform(response)
        return response, status.value[0]

    def build(self,fn_transform=None) -> Any:
        if self.response[OPERATION_ID_KEY] is None:
            self.response[OPERATION_ID_KEY] = get_operation_id()
        if fn_transform != None:
            self.response = fn_transform(self.response)
        return self.response, self.response_code

    def str_json_build(self,fn_transform) -> Any:
        if self.response[OPERATION_ID_KEY] is None:
            self.response[OPERATION_ID_KEY] = get_operation_id()
        if fn_transform != None:
            self.response = fn_transform(self.response)
        return json.dumps(self.response), self.response_code


class BResponse(Builder):
    """
    Zurck'z Common Builder Response

    """

    def err(
        payload=None,
        errors=[],
        status=Status.INTERNAL_SERVER_ERROR,
        operation_id=None,
        description: str = None,
        fn_transform=None,
    ):
        """
        Build a error response with None payload
        """
        return Builder.error(
            payload, errors, status, operation_id, description, fn_transform
        )
