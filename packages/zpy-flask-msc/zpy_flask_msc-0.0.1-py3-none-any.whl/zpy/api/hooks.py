from abc import ABC, abstractmethod
from flask import request
from zpy.logger import g_log
from zpy.api.errors import ErrorBuilder
from flask import Flask
from zpy.utils.Encryptor import AESEncryptor
from zpy.api.stages import Encryption, ResourceGateway
from zpy.api.reponse import Builder, Status
import json

__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "upax"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


class ZHook(ABC):
    @abstractmethod
    def execute(self, app: Flask, **kwargs):
        pass


# Custom hooks


class AESEncryptHook(ZHook):
    def execute(self, app, **kwargs):
        @app.after_request
        def encrypt(response: Flask):
            try:
                if response.data:
                    parsed = json.loads(response.data)
                    aes: str = None
                    if (
                        kwargs != None and "aes_sk" in kwargs
                    ):  # ! WARNING HARD KEY FOR EXTARCT AES SK
                        aes = kwargs["aes_sk"]
                    encrypted = AESEncryptor.encrypt_ws_request(parsed, secret_key=aes)
                    response.data = json.dumps(encrypted)
                return response
            except Exception as e:
                stage = Encryption()
                g_log(e, stage)
                return Builder().error(
                    {},
                    errors=[
                        ErrorBuilder.common(
                            "Encryption hook throw exception",
                            "The response catched by hook have invalid structure",
                            stage,
                        )
                    ],
                )

        return super().execute(app)


class AESDecryptHook(ZHook):
    def execute(self, app: Flask, **kwargs):
        @app.before_request
        def decrypt():
            try:
                if request.data:
                    aes: str = None
                    if (
                        kwargs != None and "aes_sk" in kwargs
                    ):  # ! WARNING HARD KEY FOR EXTARCT AES SK
                        aes = kwargs["aes_sk"]
                    decrypt_data = AESEncryptor.decrypt_ws_response(
                        request.get_json(), aes
                    )
                    request.data = json.dumps(decrypt_data)
                return request
            except Exception as e:
                stage = Encryption()
                g_log(e, stage)
                return Builder().error(
                    {},
                    errors=[
                        ErrorBuilder.common(
                            "Encryption hook throw exception",
                            "The response catched by hook have invalid structure",
                            stage,
                        )
                    ],
                )

        return super().execute(app)


class NotFoundHook(ZHook):
    def execute(self, app: Flask, **kwargs):
        @app.errorhandler(404)
        def not_found(e):
            try:
                g_log(e, ResourceGateway())
                return (
                    Builder()
                    .add_status(Status.NOT_FOUND)
                    .add_error("Resource not exist")
                    .add_error(str(e))
                    .build()
                )
            except Exception:
                pass

        return super().execute(app)


class TearDownHook(ZHook):
    def execute(self, app: Flask, **kwargs):
        @app.teardown_appcontext
        def dispose(exception):
            try:
                print("Teardown Micro Service")
            except Exception:
                pass

        return super().execute(app)
