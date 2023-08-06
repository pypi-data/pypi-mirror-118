from abc import ABC, abstractmethod
from typing import Any, List

from zpy.custom.models import DBSSMCredentialsModel, SSMConstants
from zpy.cloud.aws.ssm import SSMParameter
from zpy.api import ApiConfiguration
from zpy.db import DBConnection
from zpy.db.oracle import OracleDB
import logging
import os


class Plugin(ABC):
    @abstractmethod
    def initialize(self, config: ApiConfiguration, ssm: SSMParameter, *args):
        pass


# Receive this by parameter where use
# class TradeConstants(Enum):
#     SSM_PREFIX = "/aws/reference/secretsmanager/com/upax/trade"
#     LOCAL_DB_SSM = "/db/oracle/zeuststtrade"
#     DB_SSM = "/db/oracle/usrtrade"
#     AES_SK_SSM = "/security/encryption"
#     AWS_SSM = "/aws/services"


# Database Schemas for Trade Project
DB_SCHEMES = [
    {"env": "prod", "value": "TRADE"},
    {"env": "qa", "value": "TRADE"},
    {"env": "dev", "value": "TRADE"},
    {"env": "localdev", "value": "ZEUSTSTTRADE"},
]

# Response modifier acordin zcommons procesor

custom_response_mapper = lambda r: {"message": r}


def pool_initialize(config: ApiConfiguration):
    """
    Initialization of the connection db connection pool and
    local client in case we are in local dev environment.
    """
    db: DBConnection = OracleDB(
        config=config.to_dict(), schemas=DB_SCHEMES, env=config.ENVIRONMENT
    )

    try:
        if config.ENVIRONMENT == "localdev":
            db.init_local_client(os.getenv("LOCAL_CLIENT"))
        db.initialize_pool(
            dns=db.get_tsn_dsn_conenction(config.to_dict(), "DSN"),
            homogeneous=True,
            user=config.DB_USER,
            pwd=config.DB_PASSWORD,
        )
    except Exception as e:
        print(e)
    return db


def setup_env(vars: dict):
    for k in vars.keys():
        os.environ[k] = vars[k]


def load_plugins(
    plugins: List[Plugin] = [],
    args_plugs: List[List[Any]] = [],
    env: str = None,
    ssm_const: SSMConstants = None,
):
    try:
        environment = os.getenv("env") if env == None else env
        if environment == None:
            raise Exception(
                "Environment not found. set environment variable with name: 'env'  and value: 'prod|qa|dev|localdev' "
            )
        if ssm_const == None:
            raise Exception("SSM Constants cannot be null, set ssm constants: see: ")
        ssm = SSMParameter(with_profile=True, prefix=ssm_const.smm_prefix)
        db_prefix = (
            ssm_const.local_db_ssm if environment == "localdev" else ssm_const.db_smm
        )
        db_credentials: DBSSMCredentialsModel = ssm.get(prefix=db_prefix, model=DBSSMCredentialsModel)
        # setup_env(db_credentials)
        aes_credentials = ssm.get(prefix=ssm_const.aes_sk)
        # setup_env(aes_credentials)
        config: ApiConfiguration = ApiConfiguration()
        config.DB_URI = db_credentials.uri
        config.DB_PASSWORD = db_credentials.password
        config.DB_PORT = db_credentials.port
        config.DB_SERVICE = db_credentials.service
        config.DB_USER = db_credentials.user
        config.ENVIRONMENT = os.getenv("env")
        config.SECRET = os.getenv("API_SECRET")
        config.CUSTOM = aes_credentials
        plugins_result = []
        for i, plugin in enumerate(plugins):
            args = args_plugs[i] if i < len(args_plugs) else {}
            plugins_result.append(plugin().initialize(config=config, ssm=ssm, **args))
        return (config, plugins_result)
    except Exception as e:
        logging.exception(e)


def setup_microservice(
    plugins: List[Plugin] = [],
    args_plugs: List[List[Any]] = [],
    env: str = None,
    ssm_const: SSMConstants = None
):
    """

    Deprecated function, will be remove in 1.0.0 core version.
    Use instead load_plugins function.

    """
    try:
        environment = os.getenv("env") if env == None else env
        if environment == None:
            raise Exception(
                "Environment not found. set environment variable with name: 'env'  and value: 'prod|qa|dev|localdev' "
            )
        if ssm_const == None:
            raise Exception("SSM Constants cannot be null, set ssm constants: see: ")
        ssm = SSMParameter(with_profile=True, prefix=ssm_const.smm_prefix)
        db_prefix = (
            ssm_const.local_db_ssm
            if environment == "localdev"
            else ssm_const.db_smm
        )
        db_credentials: DBSSMCredentialsModel = ssm.get(prefix=db_prefix, model=DBSSMCredentialsModel)
        # setup_env(db_credentials)
        aes_credentials = ssm.get(prefix=ssm_const.aes_sk)
        setup_env(aes_credentials)
        config: ApiConfiguration = ApiConfiguration()
        config.DB_URI = db_credentials.uri
        config.DB_PASSWORD = db_credentials.password
        config.DB_PORT = db_credentials.port
        config.DB_SERVICE = db_credentials.service
        config.DB_USER = db_credentials.user
        config.ENVIRONMENT = os.getenv("env")
        config.SECRET = os.getenv("API_SECRET")
        db: DBConnection = pool_initialize(config)
        plugins_result = []
        for i, plugin in enumerate(plugins):
            plugins_result.append(
                plugin().initialize(config=config, ssm=ssm, *args_plugs[i])
            )

        return (config, db, plugins_result)
    except Exception as e:
        logging.exception(e)
