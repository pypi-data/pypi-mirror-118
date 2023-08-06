from zpy.api.errors import ErrorBuilder

__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "upax"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


class ZError(Exception):
    """
    ZPy Base Error
    """

    CUSTOM_MESSAGE: str = (
        "An uncontrolled, developer-unspecified error has been generated"
    )
    custom_message: str = None
    custom_reason: str = None
    exception_data: Exception = None

    def get_error(self):
        return ErrorBuilder.common(
            reason= self.custom_reason,
            message= self.get_message(),
        )

    def get_message(self):
        return (
            self.CUSTOM_MESSAGE if self.custom_message == None else self.custom_message
        )

    def get_exception(self):
        if self.exception_data == None:
            msg = (
                self.CUSTOM_MESSAGE
                if self.custom_message == None
                else self.custom_message
            )
            return Exception(msg)
        return self.exception_data

    def __init__(
        self,
        message: str = None,
        d_except: Exception = None,
        reason: str = None,
        *args: object
    ) -> None:
        super().__init__(*args)
        self.custom_message = message
        self.exception_data = d_except
        self.custom_reason = reason


class ZRepositoryError(ZError):
    """
    General Repository Layer Error
    """

    CUSTOM_MESSAGE = "[RP-00] An error was generated in the data access layer when performing operations with the provided data."

    def __init__(
        self,
        message: str = None,
        d_except: Exception = None,
        reason: str = None,
        *args: object
    ) -> None:
        super().__init__(message=message, d_except=d_except, reason=reason, *args)

    """
    General Service Layer Error
    """

    CUSTOM_MESSAGE = (
        "[SE-00] An error was generated when try execute logics with data supplied"
    )

    def __init__(
        self,
        message: str = None,
        d_except: Exception = None,
        reason: str = None,
        *args: object
    ) -> None:
        super().__init__(message=message, d_except=d_except, reason=reason, *args)


class ZUnavailableError(ZError):
    """
    Unavaible Error
    """

    CUSTOM_MESSAGE = "[UE-00] An error was generated when trying to interact with some entity and it is not available"

    def __init__(
        self,
        message: str = None,
        d_except: Exception = None,
        reason: str = None,
        *args: object
    ) -> None:
        super().__init__(message=message, d_except=d_except, reason=reason, *args)


class ZDatabaseOperationError(ZError):
    """
    Database error
    """

    CUSTOM_MESSAGE = "[RP-DB-00] An error was generated when interacting with the data provider when performing an operation on the schema with the data provided"

    def __init__(
        self,
        message: str = None,
        d_except: Exception = None,
        reason: str = None,
        *args: object
    ) -> None:
        super().__init__(message=message, d_except=d_except, reason=reason, *args)


class ZDBIntegrityError(ZError):
    """
    * Integrity database violated error
    """

    CUSTOM_MESSAGE = "[RP-DB-01] An error was generated in the data provider, the integrity of the schema was violated by some operation carried out with the data provided"

    def __init__(
        self,
        message: str = None,
        d_except: Exception = None,
        reason: str = None,
        *args: object
    ) -> None:
        super().__init__(message=message, d_except=d_except, reason=reason, *args)


class ZResourceError(ZError):
    """
    Resource exception
    """

    CUSTOM_MESSAGE = "[RS-00] An error was generated on the resource layer when it try execute some operation [Validation, Request Extraction, Response Building...]"

    def __init__(
        self,
        message: str = None,
        d_except: Exception = None,
        reason: str = None,
        *args: object
    ) -> None:
        super().__init__(message=message, d_except=d_except, reason=reason, *args)