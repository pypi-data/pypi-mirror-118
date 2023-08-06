from abc import ABC, abstractmethod
from zpy.api.reponse import Builder
from zpy.api.stages import Decrypt
from zpy.logger import g_log
from zpy.api.errors import ErrorBuilder
from flask import Flask
from typing import Any
from flask.wrappers import Request, Response
from zpy.utils.Encryptor import AESEncryptor
import json


__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "upax"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


# Middlewares | Zurck'Z Middlware
# Base middleware for flask
class ZMiddleware(ABC):
    def __init__(self, app: Flask, **kwargs) -> None:
        super().__init__()
        self.app = app
        self.kwargs = kwargs

    @abstractmethod
    def __call__(self, environ: Any, start_response: Any) -> Any:
        return self.app(environ, start_response)


# Custom Middlewares
# Encrypt body of responses with AES algorithm
class EncryptMiddleWare(ZMiddleware):
    def __init__(self, app: Flask, **kwargs) -> None:
        super().__init__(app, **kwargs)
        self.app = app

    def __call__(self, environ: Any, start_response: Any) -> Any:
        response = Response(environ)
        return super().__call__(environ, start_response)
        # return response(environ,start_response)


# Custom Middlewares
# Encrypt body of responses with AES algorithm
class DecryptMiddleWare(ZMiddleware):
    def __init__(self, app: Flask, **kwargs):
        super().__init__(app, **kwargs)
        self.app = app

    def __call__(self, environ, start_response):
        try:
            if environ["request"]:
                aes: str = None
                if (
                    self.kwargs != None and "aes_sk" in self.kwargs
                ):  # ! WARNING HARD KEY FOR EXTARCT AES SK
                    aes = self.kwargs["aes_sk"]
                encrypt_data = environ["request"]
                decrypt_data = AESEncryptor.decrypt_ws_response(
                    encrypt_data, secret_key=aes
                )
                environ["request"] = decrypt_data
            return self.app(environ, start_response)
        except Exception as e:
            stage = Decrypt()
            g_log(e, stage)
            res = Response(
                json.dumps(
                    Builder.error(
                        errors=[
                            ErrorBuilder().common(
                                "Threw exception on decrypt process",
                                "Request supplied not have a valid format",
                                stage,
                            )
                        ]
                    )
                ),
                mimetype="text/json",
                status=500,
            )
            return res(environ, start_response)


class ParserMiddleWare(ZMiddleware):
    """
    Default middleware for custom access response
    """

    def __init__(self, app: Flask, **kwargs):
        super().__init__(app, **kwargs)
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        try:
            if request.data:
                environ["request"] = json.loads(request.data)
            else:
                environ["request"] = None
            return self.app(environ, start_response)
        except Exception as e:
            stage = Decrypt()
            g_log(e, stage)
            res = Response(
                json.dumps(
                    Builder.error(
                        errors=[
                            ErrorBuilder().common(
                                "Threw exception on decrypt process",
                                "Request supplied not have a valid format",
                                stage,
                            )
                        ]
                    )
                ),
                mimetype="text/json",
                status=500,
            )
            return res(environ, start_response)
