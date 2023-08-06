from typing import Dict
from zpy.api import ApiConfiguration


class DevConfigurations(ApiConfiguration):
    DEBUG: bool = True
    TESTING: bool = True
    CSRF_ENABLED: bool = False
    SECRET: str = ""
    DB_URI: str = ""
    DB_SERVICE: str = ""
    DB_PORT: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    ENVIRONMENT: str = "local_dev"
    CUSTOM: Dict = {}


apiConfig = DevConfigurations()