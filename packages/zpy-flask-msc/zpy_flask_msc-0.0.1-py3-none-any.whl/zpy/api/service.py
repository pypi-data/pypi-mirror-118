__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


from zpy.api.repository import RepositoryResult
from typing import Any, List, TypeVar
from zpy.api import ZContract, ZContractStatus
from zpy.api.reponse import Status

T = TypeVar("T")


class ServiceResult(ZContract[T]):
    http_status: Status

    def __init__(
        self,
        data: T = None,
        status: ZContractStatus = ZContractStatus.PENDING ,
        errors: List[Any] = None,
        http_status: Status = Status.SUCCESS,
    ) -> None:
        super().__init__(data=data, status=status, errors=errors)
        self.http_status = http_status


class ZService:
    def __init__(self) -> None:
        print(f"Zurck'z  - Core Service was iniitalized")

    def either_error(self, errors: List[dict], result: RepositoryResult) -> T:
        if result.status == ZContractStatus.ERROR:
            errors.extend(result.errors)
        return result.data