from datetime import datetime
import uuid
import os

__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "upax"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"

# Date utils
str_date = lambda str_date, format="%Y-%m-%d": datetime.strptime(str_date, format)
date_str = lambda date_time, format="%Y-%m-%d %H:%M:%S": date_time.strftime(format)
get_date = lambda: datetime.now()


def add_hours_to_date(date: str, time: str):
    """
    date: 2020-10-10
    time: 10:50:00
    """
    dte = str_date(date)
    splitted_time = time.split(r":")
    size = len(splitted_time)
    nwdte = None
    try:
        if size >= 3:
            nwdte = dte.replace(
                hour=int(splitted_time[0]),
                minute=int(splitted_time[1]),
                second=int(splitted_time[2]),
            )
        elif size == 2:
            nwdte = dte.replace(
                hour=int(splitted_time[0]), minute=int(splitted_time[1]), second=0
            )
        else:
            nwdte = dte.replace(hour=int(splitted_time[0]), minute=0, second=0)
    except Exception as e:
        nwdte = dte.replace(hour=0, minute=0, second=0)

    return nwdte


# Environment utils
def env(key: str):
    """
    Get environment value by key
    """
    try:
        return os.getenv(key)
    except Exception as e:
        return None


def find(list, filter):
    for x in list:
        if filter(x):
            return x
    return None


def get_operation_id() -> str:
    return str(uuid.uuid1())