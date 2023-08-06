from zpy.api.stages import Stage
from io import StringIO
from enum import Enum
import logging

FORMAT = "ZR: %(asctime)s - %(name)s - %(levelname)s - %(message)s"
# logging.basicConfig(format=FORMAT)


class LColors(Enum):
    CEND = "\033[0m"
    CBLACK = "\33[30m"
    CRED = "\33[31m"
    CGREEN = "\33[32m"
    CYELLOW = "\33[33m"
    CBLUE = "\33[34m"
    CVIOLET = "\33[35m"
    CBEIGE = "\33[36m"
    CWHITE = "\33[37m"


def line(length: int = 100, char: str = "=") -> str:
    """
    Helper function
    """
    return "".join([char for x in range(length)])


def g_log(msg, phase: Stage):
    print(line())
    print(phase.title())
    print(phase.desc())
    print(msg)
    print(line())


def c_warn(msg, single=False, prefix: str = ""):
    if single:
        print(f"{LColors.CYELLOW.value}{prefix}{msg}{LColors.CEND.value}")
    else:
        print(f"{LColors.CYELLOW.value} [ZPy WARNING]: {msg}{LColors.CEND.value}")


def c_err(msg, single=False, prefix: str = ""):
    if single:
        print(f"{LColors.CRED.value}{prefix}{msg}{LColors.CEND.value}")
    else:
        print(f"{LColors.CRED.value} [ZPy ERROR]: {msg}{LColors.CEND.value}")


def c_info(msg, single=False, prefix: str = ""):
    if single:
        print(f"{LColors.CBLUE.value}{prefix}{msg}{LColors.CEND.value}")
    else:
        print(f"{LColors.CBLUE.value} [ZPy INFORMATION]: {msg}{LColors.CEND.value}")


def c_text(msg, single=False, prefix: str = ""):
    if single:
        print(f"{LColors.CWHITE.value}{prefix}{msg}{LColors.CEND.value}")
    else:
        print(f"{LColors.CWHITE.value} [ZPy]: {msg}{LColors.CEND.value}")


class TLogger:
    logger_name = "TradeLogger"

    def __init__(self, name=None, operation_id=None) -> None:
        self.log = logging.getLogger(self.logger_name if name is None else name)
        if self.log.handlers:
            for handler in self.log.handlers:
                self.log.removeHandler(handler)
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)
        self.handler.setFormatter(logging.Formatter(FORMAT))
        self.log.addHandler(self.handler)
        self.log.setLevel(logging.DEBUG)
        self.operation_id = operation_id
        self.log.info(line())
        self.log.info("[ START OPERATION ID :: {0}]".format(self.operation_id))
        self.log.info(line())

    def add_error(self, error) -> None:
        self.log.error(error)

    def add_exception(self, exception) -> None:
        self.log.error(exception, exc_info=True)

    def add_warning(self, warning) -> None:
        self.log.error(warning)

    def add_info(self, info) -> None:
        self.log.info(info)

    def add_phase(self, phase: Stage):
        self.log.info(line())
        self.log.info("[ STARTING STAGE]")
        self.log.info(phase.title())
        self.log.info(phase.desc())
        self.log.info(line())

    def show_stack_trace(self):
        self.log.info(line())
        print(self.stream.getvalue())

    def dispose(self):
        self.handler.close()
        self.log.removeHandler(self.handler)


def add_log_to(log: any, logger: TLogger):
    if logger != None:
        if isinstance(log, Exception):
            logger.add_exception(log)
        else:
            logger.add_info(log)