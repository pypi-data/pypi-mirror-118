from marshmallow_objects import models
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional
from copy import copy
import json


__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


#
# Zurck'z implementation
class ZModel(models.Model):
    """
    Zurckz Model
    """

    __remove_keys: List[str] = [
        "__dump_lock__",
        "__schema__",
        "__missing_fields__",
        "__setattr_func__",
        "_ZModel__remove_keys",
        "_ZModel__update_items",
    ]

    __update_items = {}

    def __init__(
        self,
        exclude: Optional[List[str]] = None,
        include: Optional[Dict[Any, Any]] = None,
        context=None,
        partial=None,
        **kwargs
    ):
        super().__init__(context=context, partial=partial, **kwargs)
        if exclude != None:
            self.__remove_keys = self.__remove_keys + exclude
        if include != None:
            self.__update_items = include

    def __str__(self):
        """
        Dump nested models by own properties
        """
        data = copy(self.__dict__)
        if self.__update_items != None:
            data.update(self.__update_items)
        [data.pop(k, None) for k in self.__remove_keys]
        for k in data.keys():
            if isinstance(data[k], models.Model):
                data[k] = json.loads(str(data[k]))
            elif isinstance(data[k], list):
                data[k] = [json.loads(str(it)) for it in data[k]]
            elif isinstance(data[k], datetime):
                data[k] = str(data[k])
        return json.dumps(data)

    def zdump(self):
        """
        Dump nested models by own properties
        """
        data = copy(self.__dict__)
        if self.__update_items != None:
            data.update(self.__update_items)
        [data.pop(k, None) for k in self.__remove_keys]
        for k in data.keys():
            if isinstance(data[k], models.Model):
                data[k] = json.loads(str(data[k]))
            elif isinstance(data[k], list):
                data[k] = [json.loads(str(it)) for it in data[k]]
            elif isinstance(data[k], datetime):
                data[k] = str(data[k])
        return data

    def sdump(
        self,
        exclude_keys: Optional[List[str]] = None,
        include: Optional[Dict[Any, Any]] = None,
        map: Optional[Callable[[Dict], Dict]] = None,
        map_args: Optional[List[Any]] = [],
        store_ex: bool = False,
        store_in: bool = False,
    ):
        """
        Model dump to json safely, checking the exclude key list

        Use this function instead of zdump.

        Parameters:
        -----------

        exclude_keys: List[str], Optional,
            List of string keys of exlude in dump process
        include: Dict[Any,Any], Optional,
            Object to include in model object after exclude process before of dump process
        map: Callable, Optional
            Callable function to tranform object after exclude and include process
        map_args: List[Any], Optional
            Argument list to passed to map callable function
        store_ex: bool, optional
            Indicate that the exclude key added to global model exclude key array
        store_in: bool, optional
            Indicate that the include object added to global model object
        """
        data = copy(self.__dict__)
        temp_exclude = copy(self.__remove_keys)
        if exclude_keys != None:
            temp_exclude = self.__remove_keys + exclude_keys
            if store_ex:
                self.__remove_keys = self.__remove_keys + exclude_keys
        [data.pop(k, None) for k in temp_exclude]
        temp_include = copy(self.__update_items)
        if include != None:
            temp_include.update(include)
            data.update(temp_include)
            if store_in:
                self.__update_items.update(include)
        else:
            if temp_include != None:
                data.update(temp_include)
        if map != None:
            data = map(data, *map_args)

        for k in data.keys():
            if isinstance(data[k], models.Model):
                data[k] = json.loads(str(data[k]))
            elif isinstance(data[k], list):
                # data[k] = [json.loads(str(it)) for it in data[k]]
                inner_list = []
                for it in data[k]:
                    if isinstance(it, str):
                        inner_list.append(it)
                    else:
                        inner_list.append(json.loads(str(it)))
                data[k] = inner_list
            elif isinstance(data[k], datetime):
                data[k] = str(data[k])
        return data

    def build(self):
        data = copy(self.__dict__)
        if self.__update_items != None:
            data.update(self.__update_items)
        [data.pop(k, None) for k in self.__remove_keys]
        return data
