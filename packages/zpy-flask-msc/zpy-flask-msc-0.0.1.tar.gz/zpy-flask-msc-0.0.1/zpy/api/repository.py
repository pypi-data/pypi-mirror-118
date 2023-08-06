from zpy.api import ZContract, ZContractStatus
from zpy.logger import TLogger, add_log_to, c_err, c_text
from zpy.api.exceptions import ZDBIntegrityError, ZDatabaseOperationError, ZError
from typing import Any, Dict, List, Optional, TypeVar
from zpy.db import DBConnection
from zpy.api.stages import DataAccess
from zpy.db.oracle import OracleType, ZParam
from zpy.db.transaction import ZOperation, ZTranstaction
import logging
import cx_Oracle

__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


T = TypeVar("T")


class RepositoryResult(ZContract[T]):
    def __init__(
        self,
        data: T = None,
        status: ZContractStatus = ZContractStatus.PENDING,
        errors: List[Any] = None,
    ) -> None:
        super().__init__(data=data, status=status, errors=errors)


class ZRepository(object):
    db: DBConnection
    logger: TLogger = None
    transact: ZTranstaction

    def __init__(self, db: DBConnection = None) -> None:
        super().__init__()
        self.db = db
        self.transact = None

    def _check_transact(self):
        if self.transact == None:
            raise "Transactionable component did not initialize."

    def set_transaction_dispatcher(self, transact: ZTranstaction):
        self.transact = transact

    def set_logger(self, logger: TLogger = None):
        self.logger = logger
        if self.logger != None:
            self.logger.add_phase(DataAccess())

    def release_db_connection(self, connection):
        if self.db != None:
            return self.db.release_connection(connection)
        raise ZDatabaseOperationError("DB Connection didn't provided")

    def get_db_connection(self, logger: TLogger = None):
        if self.db != None:
            return self.db.get_pool_connection(logger=logger)
        raise ZDatabaseOperationError("DB Connection didn't provided")

    def __show_db_error(
        self,
        e: Exception,
        fn: str,
        type_err: str,
        native_params: Dict = None,
        custom_params: Optional[List[ZParam]] = None,
        logger: TLogger = None,
    ):
        """
        Show error acording logger value, if logger is null print on console

        RETURNS:
        -------
            added into logger

        """
        logger = self.logger if logger == None else logger
        if logger == None:
            c_err("\n\tAN ERROR OCURRED WHEN EXECUTE DB FUNCTION\n", True)
            c_text(f"     Function: {fn}", True)
            c_text(f"         Type: {type_err}", True)
            c_text("  With params: {}".format(native_params), True)
            c_text("Custom params: {}".format(custom_params), True)
            c_text("--------------------------------------------------", True)
            c_text("Details:", True)
            logging.exception(e)
            c_err("--------------------------------------------------", True)
            return False
        else:
            add_log_to("\n\tAN ERROR OCURRED WHEN EXECUTE DB FUNCTION\n", logger)
            add_log_to(f"     Function: {fn}", logger)
            add_log_to(f"         Type: {type_err}", logger)
            add_log_to(f"  With params: {native_params}", logger)
            add_log_to(f"Custom params: {custom_params}", logger)
            add_log_to("--------------------------------------------------", logger)
            add_log_to("Details:", logger)
            add_log_to(e, logger)
            add_log_to("--------------------------------------------------", logger)
            return True

    def __extract_custom_errors(self, current_connection):
        try:
            cursor = current_connection.cursor()
            status = cursor.var(cx_Oracle.NUMBER)
            line = cursor.var(cx_Oracle.STRING)
            lines = []
            while True:
                cursor.callproc("DBMS_OUTPUT.GET_LINE", (line, status))
                if status.getvalue() == 0:
                    lines.append(line.getvalue())
                else:
                    break
            cursor.close()
            return lines
        except Exception as e:
            print(e)
        return []

    def __get_custom_messgae(self, e: Exception):
        try:
            stringfy = str(e)
            stringfy = stringfy[stringfy.index("::") + 2 :]
            return stringfy[: stringfy.index("::")]
        except Exception as e:
            return "Unspecified error."

    def exec(
        self,
        fn_name: str,
        ret_type: OracleType,
        params: dict = None,
        model: Any = None,
        connection=None,
        custom_params: Optional[List[ZParam]] = None,
        logger: TLogger = None,
    ) -> RepositoryResult:
        """
        DB Funtion executor

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

        ZDBException
            DB General Exception

        ZIDBException
            Vilated DB Integrity

        Returns
        -------
        result : RespositoryResult
            The result set of oracle db function
        """
        try:
            result = self.execute(
                fn_name=fn_name,
                ret_type=ret_type,
                params=params,
                model=model,
                connection=connection,
                custom_params=custom_params,
                logger=logger,
            )
            return RepositoryResult(data=result, status=ZContractStatus.SUCCESS)
        except ZError as e:
            return RepositoryResult(
                status=ZContractStatus.ERROR, errors=[e.get_error()]
            )

    def execute(
        self,
        fn_name: str,
        ret_type: OracleType,
        params: dict = None,
        model: Any = None,
        connection=None,
        custom_params: Optional[List[ZParam]] = None,
        logger: TLogger = None,
    ):
        """
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

        ZDBException
            DB General Exception

        ZIDBException
            Vilated DB Integrity

        Returns
        -------
        result set : Union[List[Model],int,float,str]
            The result set of oracle db function
        """
        logger = self.logger if logger == None else logger
        if self.db is None:
            add_log_to("DB Connection didn't provided in execute db function", logger)
            raise ZDatabaseOperationError(
                message="Impossible establish a connection with data provider.",
                reason="Connection object did not provided to dispatcher.",
            )
        cn = connection
        connection_passed = True
        if connection == None:
            connection_passed = False
            cn = self.db.get_pool_connection()
        try:
            result_set = self.db.exec(
                fn=fn_name,
                ret_type=ret_type,
                params=params,
                model=model,
                connection=cn,
                custom_params=custom_params,
            )
            if connection_passed == False:
                self.db.release_connection(cn)
            return result_set
        except cx_Oracle.IntegrityError as e:
            if connection_passed == False:
                self.db.release_connection(cn)
            if (
                self.__show_db_error(
                    e,
                    fn_name,
                    "Integrity Database Error",
                    params,
                    custom_params,
                    logger,
                )
                == False
            ):
                add_log_to(e, logger)
            raise ZDBIntegrityError(
                d_except=e,
                message=self.__get_custom_messgae(e),
                reason="A data schema restriction is violated when attempting to process operations on the supplied data.",
            )
        except Exception as e:

            if connection_passed == False:
                self.db.release_connection(cn)
            if (
                self.__show_db_error(
                    e,
                    fn_name,
                    "Unspecified DB Exception",
                    params,
                    custom_params,
                    logger,
                )
                == False
            ):
                add_log_to(e, logger)

            raise ZDatabaseOperationError(
                d_except=e,
                message=self.__get_custom_messgae(e),
                reason="When trying to process an operation with the database provider.",
            )

    def exec_txn(
        self,
        fn_name: str,
        ret_type: OracleType,
        table_name: str = None,
        operation_type=ZOperation,
        transaction: str = None,
        params: dict = None,
        model: Any = None,
        connection=None,
        custom_params: Optional[List[ZParam]] = None,
        logger: TLogger = None,
    ) -> RepositoryResult:
        self._check_transact()
        result = self.exec(
            fn_name=fn_name,
            ret_type=ret_type,
            params=params,
            model=model,
            connection=connection,
            custom_params=custom_params,
            logger=logger,
        )
        if result.status == ZContractStatus.SUCCESS:
            row = result
            if "INT" in operation_type.value:
                row = params
            else:
                if ret_type == OracleType.number or ret_type == OracleType.decimal:
                    row = {"id": result}
            self.transact.operation(operation_type, table_name, row, transaction)
        return result

    def execute_txn(
        self,
        fn_name: str,
        ret_type: OracleType,
        table_name: str = None,
        operation_type=ZOperation,
        transaction: str = None,
        params: dict = None,
        model: Any = None,
        connection=None,
        custom_params: Optional[List[ZParam]] = None,
        logger: TLogger = None,
    ) -> Any:
        """
        Can be throw exception
        """
        self._check_transact()
        result = self.execute(
            fn_name=fn_name,
            ret_type=ret_type,
            params=params,
            model=model,
            connection=connection,
            custom_params=custom_params,
            logger=logger,
        )

        if result != None:
            row = result
            if "INT" in operation_type.value:
                row = params
            else:
                if ret_type == OracleType.number or ret_type == OracleType.decimal:
                    row = {"id": result}
            self.transact.operation(operation_type, table_name, row, transaction)
        return result

    def insert(
        self,
        fn_name: str,
        ret_type: OracleType,
        table_name: str = None,
        transaction: str = None,
        params: dict = None,
        model: Any = None,
        connection=None,
        custom_params: Optional[List[ZParam]] = None,
        logger: TLogger = None,
    ) -> Any:
        """
        Zurck'z
        Can be throw an exception
        """
        self._check_transact()
        result = self.execute(
            fn_name=fn_name,
            ret_type=ret_type,
            params=params,
            model=model,
            connection=connection,
            custom_params=custom_params,
            logger=logger,
        )

        if result != None:
            row = result
            if ret_type == OracleType.number or ret_type == OracleType.decimal:
                row = {"id": result}
            self.transact.insert(table=table_name, data=row, transaction=transaction)
        return result

    def int_insert(
        self,
        fn_name: str,
        ret_type: OracleType,
        table_name: str = None,
        transaction: str = None,
        params: dict = None,
        model: Any = None,
        connection=None,
        custom_params: Optional[List[ZParam]] = None,
        logger: TLogger = None,
    ) -> Any:
        """
        Zurck'z
        Can be throw an exception
        """
        self._check_transact()
        result = self.execute(
            fn_name=fn_name,
            ret_type=ret_type,
            params=params,
            model=model,
            connection=connection,
            custom_params=custom_params,
            logger=logger,
        )

        if result != None:
            self.transact.int_insert(
                table=table_name, data=params, transaction=transaction
            )
        return result

    def update(
        self,
        fn_name: str,
        ret_type: OracleType,
        table_name: str = None,
        transaction: str = None,
        params: dict = None,
        model: Any = None,
        connection=None,
        custom_params: Optional[List[ZParam]] = None,
        logger: TLogger = None,
    ) -> Any:
        """
        Zurck'z
        Can be throw an exception
        """
        self._check_transact()
        result = self.execute(
            fn_name=fn_name,
            ret_type=ret_type,
            params=params,
            model=model,
            connection=connection,
            custom_params=custom_params,
            logger=logger,
        )

        if result != None:
            row = result
            if ret_type == OracleType.number or ret_type == OracleType.decimal:
                row = {"id": result}
            self.transact.update(table=table_name, data=row, transaction=transaction)
        return result

    def int_update(
        self,
        fn_name: str,
        ret_type: OracleType,
        table_name: str = None,
        transaction: str = None,
        params: dict = None,
        model: Any = None,
        connection=None,
        custom_params: Optional[List[ZParam]] = None,
        logger: TLogger = None,
    ) -> Any:
        """
        Zurck'z
        Can be throw an exception
        """
        self._check_transact()
        result = self.execute(
            fn_name=fn_name,
            ret_type=ret_type,
            params=params,
            model=model,
            connection=connection,
            custom_params=custom_params,
            logger=logger,
        )

        if result != None:
            self.transact.int_update(
                table=table_name, data=params, transaction=transaction
            )
        return result

    def delete(
        self,
        fn_name: str,
        ret_type: OracleType,
        table_name: str = None,
        transaction: str = None,
        params: dict = None,
        model: Any = None,
        connection=None,
        custom_params: Optional[List[ZParam]] = None,
        logger: TLogger = None,
    ) -> Any:
        """
        Zurck'z
        Can be throw an exception
        """
        self._check_transact()
        result = self.execute(
            fn_name=fn_name,
            ret_type=ret_type,
            params=params,
            model=model,
            connection=connection,
            custom_params=custom_params,
            logger=logger,
        )

        if result != None:
            row = result
            if ret_type == OracleType.number or ret_type == OracleType.decimal:
                row = {"id": result}
            self.transact.delete(table=table_name, data=row, transaction=transaction)
        return result

    def int_delete(
        self,
        fn_name: str,
        ret_type: OracleType,
        table_name: str = None,
        transaction: str = None,
        params: dict = None,
        model: Any = None,
        connection=None,
        custom_params: Optional[List[ZParam]] = None,
        logger: TLogger = None,
    ) -> Any:
        """
        Zurck'z
        Can be throw an exception
        """
        self._check_transact()
        result = self.execute(
            fn_name=fn_name,
            ret_type=ret_type,
            params=params,
            model=model,
            connection=connection,
            custom_params=custom_params,
            logger=logger,
        )

        if result != None:
            self.transact.int_delete(
                table=table_name, data=params, transaction=transaction
            )
        return result

    def begin_txn(self, name: str):
        """
        """
        self._check_transact()
        self.transact.begin_txn(name)

    def commit_txn(self, name: str = None, pop: bool = False):
        """
        """
        self._check_transact()
        return self.transact.commit(name, pop)

    def get_transaction_store(self) -> dict:
        self._check_transact()
        return self.transact.store