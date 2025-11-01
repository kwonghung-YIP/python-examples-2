from enum import Enum
from datetime import date
from uuid import UUID, uuid4
from typing import Annotated, NewType, Optional
from pydantic import BaseModel, Field

Email = NewType('Email',str)

class Title(Enum):
    MR = "Mr"
    MRS = "Mrs"
    DR = "Dr"

class Name(BaseModel):
    title: Annotated[Title|None,Field(title="Title")] = None
    firstName: Annotated[str,Field(max_length=30)]
    lastName: Annotated[str,Field(max_length=30)]

class Person(BaseModel):
    id: Annotated[UUID,Field(frozen=True,strict=True,default_factory=uuid4)]
    name: Annotated[Name,""]
    email: Annotated[Email,Field(title="Personal email")]
    dob: Annotated[Optional[date],Field(title="Date of birth")]=None

    @property
    def age(self) -> int|None:
        return None if self.dob is None else (date.today() - self.dob).days // 365.25