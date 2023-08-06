from enum import Enum
from typing import Dict
from zpy.api.stages import Unspecified


__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


class ErrorDomain(Enum):
    GLOBAL = ("GLOBAL", "")
    IN_PHASE = ("IN PHASE", "")
    INVALID_REQUEST = ("INVALID REQUEST", "")
    INVALID_PARAMETER = ("INVALID PARAMETER", "")


class ErrorCodes(Enum):
    UNSPECIFIED = 99
    GENERAL = 100
    BAD_REQUEST = 101
    INVALID_TYPE_REQUEST = 102
    DB_OPERATION = 103
    SERVICE_PROCESS = 104


# DOMAIN_ERROR_KEY   = 'domain'
REASON_ERROR_KEY = "reason"
MESSAGE_ERROR_KEY = "message"
METADATA_KEY = "metadata"
CODE_ERROR_KEY = "code"
# STAGE_ERROR_KEY    = 'stage'


class ErrorBuilder(object):
    error = {
        # DOMAIN_ERROR_KEY  : ErrorDomain.GLOBAL,
        REASON_ERROR_KEY: "",
        MESSAGE_ERROR_KEY: "",
        CODE_ERROR_KEY: "",
        # STAGE_ERROR_KEY    : Unspecified().name,
        METADATA_KEY: None,
    }

    @staticmethod
    def common(reason: str, message: str, code: ErrorCodes = ErrorCodes.GENERAL, meta=None):
        return {
            # DOMAIN_ERROR_KEY: domain.value[0],
            REASON_ERROR_KEY: reason,
            MESSAGE_ERROR_KEY: message,
            CODE_ERROR_KEY: code.value,
            METADATA_KEY: meta,
            # STAGE_ERROR_KEY: stage.name,
        }

    # def add_stage(self, stage:Stage = Unspecified()):
    #     self.error[STAGE_ERROR_KEY] = stage.name
    #     return self

    def add_meta(self, meta: Dict = Unspecified()):
        self.error[METADATA_KEY] = meta
        return self

    # def add_domain(self, domain:ErrorDomain = ErrorDomain.GLOBAL):
    #     self.error[DOMAIN_ERROR_KEY] = domain.value[0]
    #     return self

    def add_reason(self, reason: str = ""):
        self.error[REASON_ERROR_KEY] = reason
        return self

    def add_message(self, message: str = ""):
        self.error[MESSAGE_ERROR_KEY] = message
        return self

    def add_code(self, code: ErrorCodes = ErrorCodes.UNSPECIFIED):
        self.error[CODE_ERROR_KEY] = code
        return self

    def build(self) -> dict:
        return self.error