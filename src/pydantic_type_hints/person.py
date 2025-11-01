import logging
from enum import Enum
from datetime import date
from uuid import UUID, uuid4
from typing import Annotated, NewType, Optional, Any
from typing_extensions import Self
from pydantic import BaseModel, Field, \
    ValidationError, BeforeValidator, AfterValidator, PlainValidator, \
    WrapValidator, ValidatorFunctionWrapHandler, \
    model_validator, ModelWrapValidatorHandler

logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)

# deal with the raw Input and could be any abitrary object
def fieldBeforeValidator(rawInput:Any) -> Any:
    log.info("fieldBeforeValidator")
    return rawInput #retrun validated value

# the input type should align with the field
def fieldAfterValidator1(fieldValue:date) -> date:
    log.info("fieldAfterValidator - date")
    return fieldValue #return validated value

def fieldAfterValidator2(fieldValue:None) -> None:
    log.info("fieldAfterValidator - None")
    return fieldValue #return validated value

# similar to before validator but terminating validation after returning
def fieldPlainValidator(rawInput:Any) -> Any:
    log.info("fieldPlainValidator")
    return rawInput

def fieldWrapValidator(rawInput:Any, handler:ValidatorFunctionWrapHandler) -> Any:
    try:
        log.info("fieldWrapValidator - before")
        # call other validator
        validated = handler(rawInput)
        log.info("fieldWrapValidator - after")
        return validated
    except ValidationError as err:
        raise

# Wrap + (Plain or Before+After)
DateOfBirth = Annotated[Optional[date], 
                AfterValidator(fieldAfterValidator2),
                AfterValidator(fieldAfterValidator1),
                BeforeValidator(fieldBeforeValidator),
                #PlainValidator(fieldPlainValidator),
                WrapValidator(fieldWrapValidator),
                ]

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
    dob: Annotated[DateOfBirth,Field(title="Date of birth")]=None

    @property
    def age(self) -> int|None:
        return None if self.dob is None else (date.today() - self.dob).days // 365.25
    
    @model_validator(mode="before")
    @classmethod
    def modelBeforeValidator(cls,rawInput:Any) -> Any:
        log.info("modelBeforeValidator")
        log.info(rawInput)
        return rawInput


    @model_validator(mode="after")
    def modelAfterValidator(self) -> Self:
        log.info("modelAfterValidator")
        return self

    @model_validator(mode="wrap")
    @classmethod
    def modelWrapValidator(cls,rawInput:Any,handler:ModelWrapValidatorHandler[Self]) -> Self:
        try:
            log.info("modelWrapValidator - before")
            validated = handler(rawInput)
            log.info(validated)
            log.info("modelWrapValidator - after")
            return validated
        except ValidationError as err:
            raise