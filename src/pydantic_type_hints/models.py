from pydantic import BaseModel
from enum import Enum
from typing import NewType

class SimpleModel(BaseModel):
    intField: int|None = None
    strField: str|None = None

type Email = str
PostCode = NewType('PostCode',str)

class Title(Enum):
    MR = "Mr"
    MRS = "Mrs"

class Name(BaseModel):

    def __init__(self,firstName:str,lastName:str,title:Title|None = None):
        self._title: Title = title
        self._firstName: str = firstName
        self._lastName: str = lastName

    @property
    def title(self) -> Title:
        return self._title
    
    @property
    def firstName(self) -> str:
        return self._firstName
    
    @firstName.setter
    def firstName(self,firstName:str) -> None:
        self._firstName = firstName

    @property
    def lastName(self) -> str:
        return self._lastName
    
class Address(BaseModel):
    flat: str
    building: str
    house: str
    street: str
    city: str
    country: str
    postcode: PostCode

class Person(BaseModel):
    name: Name
    age:int|None = None

    #def __init__(self,name:Name,age:int|None = None):
        #self._name = Name
        #self._age = age

    #@property
    #def age(self) -> int:
    #    return _age
