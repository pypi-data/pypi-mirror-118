from abc import ABC, abstractmethod
from zpy.logger import TLogger
from typing import Any, Dict, Optional, TypeVar
from marshmallow_objects import models


T = TypeVar("T")


class DBConnection(ABC):
    @abstractmethod
    def init_local_client(self, path: str):
        """
        Initialize local client
        """
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def is_connected(self):
        pass

    @abstractmethod
    def get_connection(self):
        pass

    @abstractmethod
    def execute(
        self,
        function: str,
        type,
        parameters: dict = None,
        pool_connection=None,
    ):
        pass

    @abstractmethod
    def get_pool_connection(self, logger: TLogger):
        pass

    @abstractmethod
    def release_connection(self, connection) -> bool:
        pass

    @abstractmethod
    def call(self, fn: str, type, params, schmea: T):
        pass

    @abstractmethod
    def close_pool(self):
        pass

    @abstractmethod
    def initialize_pool(
        self,
        dns=None,
        homogeneous: bool = False,
        max: int = 5,
        user=None,
        pwd=None,
        min: int = 1,
        threaded: bool = False,
    ):
        pass

    @abstractmethod
    def exec(
        self,
        fn: str,
        ret_type: Any,
        params: Optional[Dict] = None,
        model: Optional[models.Model] = None,
        connection=None,
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
        pass