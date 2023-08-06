from zpy.logger import TLogger, c_info
from zpy.db.utils import get_current_schema
from marshmallow_objects import models
from typing import Any, Dict, List, Optional, Union
from zpy.db import DBConnection
from zpy.utils.funcs import exec_ifnt_null, safely_exec
from enum import Enum
from marshmallow import Schema
import cx_Oracle
import json
import logging

# from . import T


__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


class OracleType(Enum):
    cursor = cx_Oracle.CURSOR
    number = cx_Oracle.NUMBER
    string = cx_Oracle.STRING
    integer = cx_Oracle.NUMBER
    decimal = cx_Oracle.NUMBER


class OracleParam(Enum):
    LIST_INTEGR = "LIST_INTEGER"
    LIST_STR = "LIST_VARCHAR"
    LIST_CLOB = "LIST_CLOB"


class ZParam:
    def __init__(
        self,
        value: Union[List[int], List[float], List[str], List[Any]],
        paramType: OracleParam,
        key: str,
        origin: str = None,
    ) -> None:
        self.value = value
        self.paramType = paramType
        self.key = key
        self.origin = origin


class IntList(ZParam):
    def __init__(self, value: List[int], key: str, origin: str = None) -> None:
        super().__init__(value, OracleParam.LIST_INTEGR, key, origin)


class StrList(ZParam):
    def __init__(self, value: List[str], key: str, origin: str = None) -> None:
        super().__init__(value, OracleParam.LIST_STR, key, origin)


class ClobList(ZParam):
    def __init__(self, value: List[Any], key: str, origin: str) -> None:
        super().__init__(value, OracleParam.LIST_CLOB, key, origin)


class OracleDB(DBConnection):
    __local_client_initialized: bool = False
    __local_client_path: str = None
    __config_connection: dict = None
    __connection = None
    __is_connected: bool = False
    __pool = None
    __pool_created: bool = False
    __schemas: List[Dict] = None
    __env: str = None
    __verbose: bool = False

    # * Pool configurations
    __max: int = 5
    __min: int = 1
    __threading: bool = False
    __homogeneus: bool = True

    def __init__(
        self,
        config: dict = None,
        local_client_path: str = None,
        schemas: List[Dict] = None,
        env: str = None,
        verbose: bool = False,
    ) -> None:
        self.__local_client_path = local_client_path
        self.__config_connection = config
        self.__schemas = schemas
        self.__env = env
        self.__verbose = verbose

    def init_local_client(self, path: str):
        if self.__local_client_initialized:
            return
        value = path if self.__local_client_path is None else self.__local_client_path
        try:
            if value is None:
                raise Exception("Local client path not provided.")
            cx_Oracle.init_oracle_client(lib_dir=value)
            self.__local_client_initialized = True
        except Exception as e:
            self.__local_client_initialized = False
            logging.exception(e)

    def __data_connection_checker(self, config: dict = None, mode="TSN") -> str:
        values = (
            config if self.__config_connection is None else self.__config_connection
        )
        if values is None:
            raise Exception("The data for the connection was not provided")
        server = values["DB_URI"]
        port = values["DB_PORT"]
        service = values["DB_SERVICE"]
        user = values["DB_USER"]
        password = values["DB_PASSWORD"]
        if mode == "DSN":
            return "{0}:{1}/{2}".format(server, port, service)
        return "{0}/{1}@{2}:{3}/{4}".format(user, password, server, port, service)

    def get_tsn_dsn_conenction(self, config: dict, mode="TSN") -> str:
        return self.__data_connection_checker(config, mode)

    def connect(self, config: dict = None):
        """
        Start oracle connection
        """
        if self.__is_connected:
            return True
        try:
            str_connection = self.__data_connection_checker(config)
            self.__connection = cx_Oracle.connect(str_connection)
            self.__is_connected = True
            return True
        except Exception as e:
            raise e

    def close(self):
        if self.__is_connected:
            self.__connection.close()
            self.__is_connected = False
            self.is_connected = False

    def is_connected(self) -> bool:
        return self.__is_connected

    def get_connection(self):
        return self.__connection

    def initialize_pool(
        self,
        dns=None,
        homogeneous: bool = False,
        max: int = 5,
        user=None,
        pwd=None,
        min: int = 1,
        threaded: bool = False,
    ) -> bool:
        if self.__pool_created or dns is None:
            return False
        print("Initializing Pool")
        self.__pool = cx_Oracle.SessionPool(
            user=user,
            password=pwd,
            dsn=dns,
            homogeneous=homogeneous,
            encoding="UTF-8",
            max=max,
            min=min,
            threaded=threaded,
        )
        self.__pool_created = True
        self.__min = min
        self.__max = max
        self.__threading = threaded
        self.__homogeneus = homogeneous
        print("Pool Started Successfuly")
        return True

    def close_pool(self, force: bool = False):
        try:
            if self.__pool_created:
                self.__pool.close(force=force)
                self.__pool_created = False
                print("Pool Closed Successfuly")
        except Exception as e:
            logging.exception(e)

    def get_pool_connection(self, logger: TLogger = None):
        if self.__pool_created:
            return self.__pool.acquire()
        exec_ifnt_null(
            lambda l: l.add_info("DB POOL NOT INITILIZED, TRY INITIALIZE AGAIN"),
            args=[logger],
        )
        try:
            self.initialize_pool(
                dns=self.get_tsn_dsn_conenction(self.__config_connection, "DSN"),
                homogeneous=self.__homogeneus,
                user=self.__config_connection["DB_USER"],
                pwd=self.__config_connection["DB_PASSWORD"],
                max=self.__max,
                min=self.__min,
                threaded=self.__threading,
            )
            self.__pool_created = True
            return self.__pool.acquire()
        except Exception as e:
            logger.add_exception(e)
            self.__pool_created = False

    def release_connection(self, connection) -> bool:
        try:
            if self.__pool_created:
                self.__pool.release(connection)
                return True
        except Exception as e:
            print("CATCH EXCEPTION WHEN TRY RELEASE POOL CONNECTION")
            logging.exception(e)
            return False

    def __proccess_result(self, result_set, type: OracleType, schema: Schema = None):
        if type == OracleType.cursor:
            columns = [field[0] for field in result_set.description]
            if schema is None:
                columns = [field[0] for field in result_set.description]
                rows = [d for d in result_set]
                data = [dict(zip(columns, row)) for row in rows]
                for d in data:
                    for key, value in d.items():
                        if isinstance(d[key], cx_Oracle.LOB):
                            d[key] = json.loads(str(value))
                return {"hasError": False, "data": json.dumps(data, default=str)}
            else:
                # [print(dict(zip(columns, r))) for r in result_set]
                return [schema.load(dict(zip(columns, r))) for r in result_set]
        elif OracleType.number:
            try:
                return float(result_set)
            except:
                return result_set
        else:
            return str(result_set)

    def execute(
        self,
        function: str,
        type: OracleType,
        parameters: dict = None,
        pool_connection=None,
    ):
        """
        Execute or call oracle functions - FN v0.0.1 | Core v0.0.1
        """
        if pool_connection is not None:
            cursor = pool_connection.cursor()
        else:
            cursor = self.__connection.cursor()
        if self.__verbose:
            self.show_info(function, parameters, type, None, None, None)
        try:
            db_execute = (
                cursor.callfunc(function, type.value, keywordParameters=parameters)
                if parameters != None
                else cursor.callfunc(function, type.value)
            )
            if type == OracleType.cursor:
                columns = [field[0] for field in db_execute.description]
                rows = [d for d in db_execute]
                data = [dict(zip(columns, row)) for row in rows]
                for d in data:
                    for key, value in d.items():
                        if isinstance(d[key], cx_Oracle.LOB):
                            d[key] = json.loads(str(value))
                db_dto = {"hasError": False, "data": json.dumps(data, default=str)}
            elif OracleType.number:
                db_dto = {"hasError": False, "data": str(db_execute)}
            else:
                db_dto = {"hasError": False, "data": db_execute}
        except Exception as e:
            db_dto = {"hasError": True, "data": str(e)}
        safely_exec(lambda c: c.close(), args=[cursor])  # * Close cursor
        return db_dto

    def call(
        self,
        fn: str,
        type: OracleType,
        params: dict,
        schema: Schema = None,
        pool_connection=None,
    ):
        """
        Execute or call oracle functions - FN v0.0.1 | Core v0.0.2
        """
        if pool_connection is not None:
            cursor = pool_connection.cursor()
        else:
            cursor = self.__connection.cursor()

        if self.__verbose:
            self.show_info(fn, params, type, schema, None, None)

        result_set = (
            cursor.callfunc(fn, type.value, keywordParameters=params)
            if params != None
            else cursor.callfunc(fn, type.value)
        )
        safely_exec(lambda c: c.close(), args=[cursor])  # * Close cursor
        return self.__proccess_result(result_set, type, schema)

    def exec(
        self,
        fn: str,
        ret_type: OracleType,
        params: Optional[Dict] = None,
        custom_params: Optional[List[ZParam]] = None,
        model: Optional[models.Model] = None,
        connection=None,
        db_schema: str = None,
        env: str = None,
    ):
        """
        Execute or call oracle functions - FN v0.0.1 | Core v0.0.7

        New feature for call oracle db functions
        Use this function instead function 'call'

        Parameters
        ----------
        fn : str | required
            Function name with package name: PO_LINES_PKG.FN_GET_LINE

        ret_type : OracleType | required
            The return type of oracle db function

        params : Dict | Optional
            Set parameter that the oracle funtion expects

        custom_params : Optional[List[ZParam, IntList, StrList, ClobList]] | Optional
            Custom Set parameter that the oracle funtion expects, see avaialble custom types

        model : marshmallow_objects.models.Model | Optional
            Model specification where the db data will be volcated

        connection : DB Connection | Optional
            The db connection object, if it is not passed by params, it tries to get a global instance

        Raises
        ------
        NotValueProvided
            Connection

        Returns
        -------
        result set : Union[List[Model],int,float,str]
            The result set of oracle db function
        """
        cursor = None
        if connection is not None:
            cursor = connection.cursor()
        else:
            cursor = self.__connection.cursor()
        if connection is None:
            raise Exception("Can't get db connection")

        if db_schema is None and self.__schemas is not None:
            db_schema = get_current_schema(self.__schemas, env, self.__env)

        if custom_params != None and len(custom_params) > 0:
            if params == None:
                params = {}
            # * Find the current env for extract the schema
            for custom in custom_params:
                params[custom.key] = self.__custom_param(
                    connection,
                    paramType=custom.paramType,
                    value=custom.value,
                    schema=db_schema,
                )

        fn = (
            fn
            if db_schema is None or db_schema.replace(" ", "") == ""
            else f"{db_schema}.{fn}"
        )
        if self.__verbose:
            self.show_info(fn, params, ret_type, model, db_schema, env)
        result_set = (
            cursor.callfunc(fn, ret_type.value, keywordParameters=params)
            if params != None
            else cursor.callfunc(fn, ret_type.value)
        )
        safely_exec(lambda c: c.close(), args=[cursor])
        return self.__proccess_result_set(result_set, ret_type, model)

    def __proccess_result_set(
        self, result_set, ret_type: OracleType, model: models.Model = None
    ):
        """
        New version of result set processor
        """
        if ret_type == OracleType.cursor:
            columns = [field[0] for field in result_set.description]
            if model is None:
                columns = [field[0] for field in result_set.description]
                rows = [d for d in result_set]
                data = [dict(zip(columns, row)) for row in rows]
                for d in data:
                    for key, value in d.items():
                        if isinstance(d[key], cx_Oracle.LOB):
                            d[key] = json.loads(str(value))
                return {"data": json.dumps(data, default=str)}
            else:
                return [model(**dict(zip(columns, r))) for r in result_set]
        elif OracleType.number:
            try:
                return float(result_set)
            except:
                return result_set
        elif OracleType.integer:
            try:
                return int(result_set)
            except:
                return result_set
        elif OracleType.decimal:
            try:
                return float(result_set)
            except:
                return result_set
        else:
            return str(result_set)

    def __custom_param(
        self,
        connection: Any,
        paramType: OracleParam,
        value: Union[List[int], List[float], List[str], List[Any]],
        schema: str = None,
    ):
        """
        Make custom param
        """
        db_schema = (
            "" if (schema is None or schema.replace(" ", "") == "") else f"{schema}."
        )
        list_type = connection.gettype(f"{db_schema}{paramType.value}")
        return list_type.newobject(value)

    def show_info(self, fn, params, ret_type, v_model, curr_schema, l_env):
        c_info("\n|-------------------------------------------------|\n", True)
        c_info(f"    Function Called: {fn} ", True)
        c_info("             Params: {}".format(params), True)
        c_info("        Return Type: {}".format(ret_type.value), True)
        c_info(f" Ref Volcated Model: {v_model}", True)
        c_info(f"          DB Schema: {curr_schema}", True)
        c_info(f"        Environment: P: {l_env} G: {self.__env}", True)
        c_info("\n|-------------------------------------------------|\n", True)
