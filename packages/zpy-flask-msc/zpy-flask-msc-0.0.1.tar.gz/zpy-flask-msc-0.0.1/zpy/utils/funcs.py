from typing import Any, Callable, List
import logging


def safely_exec(callable: Callable, args: List[Any] = []):
    try:
        return callable(*args)
    except Exception as e:
        logging.exception(e)
    return None


def exec_ifnt_null(callable: Callable, args: List[Any] = []):
    """
    Execute function if args not null
    """
    for arg in args:
        if arg == None:
            return False
    return callable(*args)