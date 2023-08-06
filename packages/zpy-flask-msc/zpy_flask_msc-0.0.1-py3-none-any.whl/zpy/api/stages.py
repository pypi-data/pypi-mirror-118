from abc import abstractmethod

__author__ = "Noé Cruz | contactozurckz@gmail.com"
__copyright__ = "Copyright 2021, Small APi Project"
__credits__ = ["Noé Cruz", "Zurck'z"]
__license__ = "upax"
__version__ = "0.0.1"
__maintainer__ = "Noé Cruz"
__email__ = "contactozurckz@gmail.com"
__status__ = "Dev"


class Stage():
    name = ""
    description = ""    
    def __init__(self,name,description) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    def get(self) -> str:
        return "\n[ PH: :: {0} ]\n[ PD: :: {1} ]\n".format(self.name,self.description)

    @abstractmethod
    def desc(self) -> str:
        return "[ PD: :: {0} ]".format(self.description)

    @abstractmethod
    def title(self) -> str:
        return "[ PH: :: {0} ]".format(self.name)

class Unspecified(Stage):
    name = "Unspecified Stage"
    description = "Unspecified stage by developer"
    def __init__(self,name: str=None,description: str=None) -> None:
        super().__init__(
            name=self.name if name is None else name,
            description=self.description if description is None else description
        )

class StartingCoreModule(Stage):
    name = "Starting Core Module"
    description = "Initializing core modules"
    def __init__(self,name: str=None,description: str=None) -> None:
        super().__init__(
            name=self.name if name is None else name,
            description=self.description if description is None else description
        )

class ResourceGateway(Stage):
    name = "Resource Gateway"
    description = "HTTP Resource Gateway"
    def __init__(self,name: str=None,description: str=None) -> None:
        super().__init__(
            name=self.name if name is None else name,
            description=self.description if description is None else description
        )
class Decrypt(Stage):
    name = "Decrypt Stage"
    description = "Http request decryption Stage"

    def __init__(self,name: str=None,description: str=None) -> None:
        super().__init__(
            name=self.name if name is None else name,
            description=self.description if description is None else description
        )

class SchemaValidation(Stage):
    name = "Schema Validation Stage"
    description = "Schemes or request models are validated according to the validations given"
    def __init__(self,name: str=None,description: str=None) -> None:
        super().__init__(
            name=self.name if name is None else name,
            description=self.description if description is None else description
        )

class ResourceLayer(Stage):
    name = "Resource Layer Stage"
    description = "Abstract presentation to business logic."
    def __init__(self,name: str=None,description: str=None) -> None:
        super().__init__(
            name=self.name if name is None else name,
            description=self.description if description is None else description
        )

class BusinessLogicExecution(Stage):
    name = "Business Logic Layer Stage"
    description = "Business Logic execution"
    def __init__(self,name: str=None,description: str=None) -> None:
        super().__init__(
            name=self.name if name is None else name,
            description=self.description if description is None else description
        )


class AuthenticationCheck(Stage):
    name = "Authentication Check Layer Stage"
    description = "Authentication Check"
    def __init__(self,name: str=None,description: str=None) -> None:
        super().__init__(
            name=self.name if name is None else name,
            description=self.description if description is None else description
        )

class AuthorizationCheck(Stage):
    name = "Authorization Check Layer Stage"
    description = "Authorization Check"
    def __init__(self,name: str=None,description: str=None) -> None:
        super().__init__(
            name=self.name if name is None else name,
            description=self.description if description is None else description
        )

class ServiceLayer(Stage):
    name = "Service Layer Stage"
    description = "Service Layer, all buisiness logic execute"
    def __init__(self,name: str=None,description: str=None) -> None:
        super().__init__(
            name=self.name if name is None else name,
            description=self.description if description is None else description
        )

class DataAccess(Stage):
    name = "Data Access Stage"
    description = "Data Access"
    def __init__(self,name: str=None,description: str=None) -> None:
        super().__init__(
            name=self.name if name is None else name,
            description=self.description if description is None else description
        )

class BuildingReponses(Stage):
    name = "Building Response Stage"
    description = "Building response..."
    def __init__(self,name: str=None,description: str=None) -> None:
        super().__init__(
            name=self.name if name is None else name,
            description=self.description if description is None else description
        )

class Encryption(Stage):
    name = "Encryption Stage"
    description = "Encryption Stage", "Response encryption proccess"
    def __init__(self,name: str=None,description: str=None) -> None:
        super().__init__(
            name=self.name if name is None else name,
            description=self.description if description is None else description
        )    
