

from abc import abstractmethod


__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "MIT"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


class Validation():
    field: str = None
    rule: str = None
    message: str = None

    def __init__(self,field:str ,rule: str,error_messgae: str) -> None:
        self.field = field
        self.rule = rule
        self.message = error_messgae

    def json(self) -> dict:
        try:
            return vars(self)
        except:
            return self.__dict__

    @abstractmethod    
    def validate(self) -> bool:
        return False






if __name__ == '__main__':
    validations = [
        Validation(
            'name',
            "required",
            "El nombre es requerido"
        ),
        Validation(
            'address',
            "required",
            "El nombre es requerido"
        ),
        Validation(
            'age',
            "required|number|max:40,min:21",
            "El nombre es requerido"
        )
    ]
    
    v = Validation(
            'age',
            "required|number|max:40,min:21",
            "El nombre es requerido"
        ).json()
    print(v)
    