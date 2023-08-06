from enum import Enum

class EnvironmentKeys(Enum):
    ENVIRONMENT = 'env'

    def __str__(self) -> str:
        return self.value
class Messages(Enum):
    GEN_MSG_ERROR = "[GE-00] An unspecified error was generated while the request was being processed."

    def __str__(self):
        return self.value