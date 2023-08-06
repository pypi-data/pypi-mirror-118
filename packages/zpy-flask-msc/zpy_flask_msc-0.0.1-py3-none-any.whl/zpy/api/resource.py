from zpy.constants import Messages
from typing import Any, Dict, List, Tuple, Union
from zpy.api.reponse import BResponse, Builder, Status
from zpy.api.stages import ResourceLayer
from zpy.utils import get_operation_id
from zpy.api.exceptions import ZError
from marshmallow_objects import models
from marshmallow.exceptions import ValidationError
from zpy.logger import TLogger, c_warn
from flask.views import MethodView
from flask import request
from enum import Enum
import json

__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


class HTTP_METHODS(Enum):
    GET = 1
    POST = 2
    PUT = 3
    PATCH = 4
    DELETE = 5


class ZResource(MethodView):
    __name__ = "ZResource"
    blocked_methods = []

    def __init__(self) -> None:
        super().__init__()
        print(f"Zurck'z  - Core Resource was iniitalized")

    def __method_not_allowed(self):
        return Builder().add_status(Status.METHOD_NOT_ALLOWED).build()

    def __is_not_allowed(self, method: HTTP_METHODS):
        return method in self.blocked_methods

    def get(self):
        if self.__is_not_allowed(HTTP_METHODS.GET):
            return self.__method_not_allowed()

    def post(self):
        if self.__is_not_allowed(HTTP_METHODS.POST):
            return self.__method_not_allowed()

    def put(self):
        if self.__is_not_allowed(HTTP_METHODS.PUT):
            return self.__method_not_allowed()

    def patch(self):
        if self.__is_not_allowed(HTTP_METHODS.PATCH):
            return self.__method_not_allowed()

    def delete(self):
        if self.__is_not_allowed(HTTP_METHODS.DELETE):
            return self.__method_not_allowed()

    def new_operation(self):
        """
        Create a new http operation.

        Returns:
            l Logger object
            i Operation id
        """
        operation_id = get_operation_id()
        log = TLogger(request.path, operation_id)
        log.add_phase(phase=ResourceLayer())
        if "request" in request.environ:
            log.add_info("Request:")
            log.add_info(request.environ["request"])
        return log, operation_id

    def close_operation(
        self, l: TLogger = None, e: Exception = None, failed: bool = False
    ):
        """
        Dispose current logger.

        l: TLogger
            Logger object
        e: Exception
            Exception to add into logger stream
        failed: bool
            Determine if logger stream should be printed
        """
        if l != None:
            if failed:
                l.add_exception(e)
                l.show_stack_trace()
            l.dispose()

    def get_request(self) -> dict:
        """
        Get current request

        Raises
        ------
        NotValueProvided
            If no values is set for the response or passed in as a parameter.

        Returns
        -------
        request : Dict[Any]
            Dict with request content

        """
        try:
            if "request" in request.environ and request.environ["request"] != None:
                return json.loads(request.environ["request"])
            return {}
        except Exception as e:
            return {}

    def either_validation(
        self, request: dict, model: models.Model
    ) -> Tuple[models.Model, Dict]:
        """
        Validate request acordning model specification

        Parameters
        ----------
        request : dict | required
            Request object to validate

        model : marshmallow_objects.models.Model | required
            The model specification

        Raises
        ------
        NotValueProvided
            If no values is set for the response or passed in as a parameter.

        Returns
        -------
        (model,errors) : Tuple[models.Model, Dict]
            Tuple with model and erros either the validation process

        """

        model_result: Union[List, models.Model] = None
        errors: Union[List, None] = None
        try:
            if request == None or len(request.items()) == 0:
                return None, {
                    "request": "The request was not provided, validation request error",
                    "fields": f"{model().__missing_fields__} not provided",
                }
            model_result = model(**request)
        except ValidationError as e:
            model_result = e.valid_data
            if isinstance(e.messages, Dict):
                errors = [e.messages]
            else:
                errors = e.messages
        return model_result, errors

    def success(
        self,
        payload={},
        logger: TLogger = None,
        status_code: Status = Status.SUCCESS,
        operation_id=None,
        description: str = None,
        map=None,
    ):
        """
        Build success response and dispose logger
        """
        self.close_operation(logger, None)
        return BResponse.success(payload, status_code, operation_id, description, map)

    def bad_request(
        self,
        payload=None,
        logger: TLogger = None,
        errors: List[Any] = [],
        status_code: Status = Status.BAD_REQUEST,
        operation_id=None,
        description: str = None,
        map=None,
    ):
        """
        Build bad request response and dispose logger
        """
        self.close_operation(logger, None)
        return BResponse.bad_request(
            payload, errors, status_code, operation_id, description, map
        )

    def response(
        self,
        payload={},
        logger: TLogger = None,
        errors: List[Any] = [],
        status_code: Status = Status.SUCCESS,
        operation_id=None,
        description: str = None,
        map=None,
    ):
        """
        Build any response and dispose logger
        """
        self.close_operation(logger, None)
        return BResponse.bad_request(
            payload, errors, status_code, operation_id, description, map
        )

    def handlde_exceptions(
        self,
        exception: Union[ZError, Exception],
        logger: TLogger,
        operation_id: str,
        payload=None,
        custom_errors: List[Union[str, dict]] = None,
        custom_message: str = None,
        custom_status: Status = None,
        map=None,
    ) -> Tuple[Dict, int]:
        """
        Handle exception and build error response with default or custom data

        Parameters
        ----------
        exception : Union[Exception,ZError]
            Exception object to handler

        logger : ZLogger
            Operation Logger for close operation and show trace

        operation_id: str
            Operation ID, must be the same as the initial ID of the operation

        custom_errors: Optional[List[Union[str, dict]]]
            Errors list for add in the resopnse
        custom_message: str
            Custom response description
        custom_statis: Status
            Cutom status for response
        map: Fn Map, Optional
            Response Modifier function
        Raises
        ------
        NotValueProvided
            If no values is set for the response or passed in as a parameter.

        Returns
        -------
        HttpResponse : Tuple[Dict,int]
            Response with error code or custom data

        """
        c_warn("handlde_exceptions() will be deprecated in version 1.0.0, use handle_exceptions instead.")
        return self.handle_exceptions(
            exception,
            logger,
            operation_id,
            payload,
            custom_errors,
            custom_message,
            custom_status,
            map,
        )

    def handle_exceptions(
        self,
        exception: Union[ZError, Exception],
        logger: TLogger,
        operation_id: str,
        payload=None,
        custom_errors: List[Union[str, dict]] = None,
        custom_message: str = None,
        custom_status: Status = None,
        map=None,
    ) -> Tuple[Dict, int]:
        """    
        Handlde exception and build error response with default or custom data

        Parameters
        ----------
        exception : Union[Exception,ZError]
            Exception object to handler

        logger : ZLogger
            Operation Logger for close operation and show trace

        operation_id: str
            Operation ID, must be the same as the initial ID of the operation

        custom_errors: Optional[List[Union[str, dict]]]
            Errors list for add in the resopnse
        custom_message: str
            Custom response description
        custom_statis: Status
            Cutom status for response
        map: Fn Map, Optional
            Response Modifier function
        Raises
        ------
        NotValueProvided
            If no values is set for the response or passed in as a parameter.

        Returns
        -------
        HttpResponse : Tuple[Dict,int]
            Response with error code or custom data

        """
        errors = [] if custom_errors == None else custom_errors
        final_status = (
            Status.INTERNAL_SERVER_ERROR if custom_status == None else custom_status
        )
        if isinstance(exception, ZError):
            errors.append(exception.get_error())
            logger.add_info(exception.get_message())
            self.close_operation(logger, exception, True)
            return BResponse.err(
                errors=errors,
                operation_id=operation_id,
                description=custom_message,
                status=final_status,
                payload=payload,
                fn_transform=map,
            )
        else:
            errors.append(str(Messages.GEN_MSG_ERROR))
            logger.add_info(str(Messages.GEN_MSG_ERROR))
            self.close_operation(logger, exception, True)
            return BResponse.err(
                errors=errors,
                operation_id=operation_id,
                description=custom_message,
                status=final_status,
                payload=payload,
                fn_transform=map,
            )
