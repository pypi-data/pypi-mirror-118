from enum import IntEnum
from zpy.api.hooks import NotFoundHook, ZHook
from zpy.api.middleware import ZMiddleware, ParserMiddleWare
from functools import wraps
from typing import Any, Dict, Generic, List, Optional, TypeVar
from flask.views import MethodView
from flask_restful import Api
from flask import Flask
from flask_cors import CORS


__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"

# Custom Type for typing generic functions
T = TypeVar("T")

##  Class ApiConfiguration
#   Multiple environment variables for microservices
#
class ApiConfiguration:
    DEBUG: bool = False
    TESTING: bool = False
    CSRF_ENABLED: bool = False
    SECRET: str = ""
    DB_URI: str = ""
    DB_SERVICE: str = ""
    DB_PORT: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    ENVIRONMENT: str = ""
    CUSTOM: Dict = {}

    def to_dict(self) -> dict:
        return {
            "DEBUG": self.DEBUG,
            "TESTING": self.TESTING,
            "CSRF_ENABLED": self.CSRF_ENABLED,
            "SECRET": self.SECRET,
            "DB_URI": self.DB_URI,
            "DB_SERVICE": self.DB_SERVICE,
            "DB_PORT": self.DB_PORT,
            "DB_USER": self.DB_USER,
            "DB_PASSWORD": self.DB_PASSWORD,
            "ENVIRONMENT": self.ENVIRONMENT,
            "CUSTOM": self.CUSTOM,
        }


##  Class ZResource | Zurck'z Resources
#   Resource class, contains resources and path related to it
#
class ZResource:
    """
    Micro service resource for api.
    """

    def __init__(self, path: str, resource: MethodView, **kwargs) -> None:
        self.resource = resource
        self.path = path
        self.kwargs = kwargs


def create_app(
    config: ApiConfiguration,
    resources: List[ZResource],
    main_path: str,
    path_cors_allow=None,
) -> Flask:
    """
    API Builder
    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    path_allow = path_cors_allow
    if path_cors_allow is None:
        path_allow = r"{}{}".format(main_path, "/*")
    CORS(app, resources={path_allow: {"origins": "*"}})
    api = Api(app)
    [
        api.add_resource(
            r.resource,
            "{0}{1}".format(main_path, r.path),
            resource_class_kwargs=r.kwargs,
        )
        for r in resources
    ]
    return app


def api(
    base: str = "",
    config: ApiConfiguration = None,
    middlewares: List[ZMiddleware] = [],
    middlewares_args: List[dict] = [],
    hooks: List[ZHook] = [],
    hooks_args: List[dict] = [],
    path_cors_allow=None,
) -> Flask:
    """
    Micro Service Setup
    """
    if config is None:
        raise Exception("Api Configurations were not provided")

    def callable(api_definitor) -> Flask:
        @wraps(api_definitor)
        def wrapper(*args, **kwargs) -> Flask:
            resources: List[ZResource] = api_definitor(*args, **kwargs)
            app: Flask = create_app(config, resources, base, path_cors_allow)
            middlewares.append(ParserMiddleWare)
            middlewares_args.append({})
            hooks.append(NotFoundHook)
            hooks_args.append({})
            for i, m in enumerate(middlewares):
                args = middlewares_args[i] if i < len(middlewares_args) else {}
                args.update(config.CUSTOM)
                app.wsgi_app = m(app.wsgi_app, **args)
            for i, h in enumerate(hooks):
                args = hooks_args[i] if i < len(hooks_args) else {}
                args.update(config.CUSTOM)
                h().execute(app, **args)
            return app

        return wrapper

    return callable


class ZContractStatus(IntEnum):
    ERROR = -1
    SUCCESS = 1
    PENDING = 0


class ZContract(Generic[T]):

    data: T = None
    status: ZContractStatus = None
    errors: List[Dict] = None

    def __init__(
        self,
        data: Optional[T] = None,
        status: ZContractStatus = ZContractStatus.PENDING,
        errors: Optional[List[Any]] = None,
    ) -> None:
        super().__init__()
        self.data = data
        self.status = status
        self.errors = errors
