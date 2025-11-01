import pytest
from typing import TypedDict, Sequence
from pydantic import ValidationError
from pydantic_core import ErrorDetails
from pydantic_type_hints.person import Person, Title, Name

from uuid import UUID, uuid4
from datetime import date

class ExpectedErrorDetails(TypedDict):
    field: str
    errorType: str

def assertValidationError(actual:ValidationError,
        expected:Sequence[ExpectedErrorDetails]) -> bool:
    try:
        #expected = expected if isinstance(expected,Sequence) else list[expected]
        assert actual.error_count() == len(expected),"Expected 3 validation errors"

        for i,ed in enumerate(actual.errors()):
            ed: ErrorDetails
            assert ed["loc"][0] == expected[i]["field"]
            assert ed["type"] == expected[i]["errorType"]

        return True
    except AssertionError:
        return False

class TestName:
    def test_with_invalid_param(self):
        """
        Create Name object with invalid field values, 
        expected ValidationError
        """
        title = "Value Not in Title Enum"
        firstName = "0123456789012345678901234567891"
        lastName = "0123456789012345678901234567891"

        expected:list[ExpectedErrorDetails] = [
            {'field':'title','errorType':'enum'},
            dict(field="firstName",errorType="string_too_long"),
            ExpectedErrorDetails(field="lastName",errorType="string_too_long")
        ]

        with pytest.raises(ValidationError, check=lambda e: assertValidationError(e,expected)):
            name = Name(title=title,firstName=firstName,lastName=lastName)

    
class TestPerson:

    @pytest.fixture(scope="class")
    def johnJson(self):
        return {
            "name":{
                "title":"Mr",
                "firstName":"John",
                "lastName":"Doe"
            },
            "email":"john.doe@gmail.com"
        }

    def test_incompatible_type_to_strict_field(self,johnJson:map):
        """
        incompatible type pass to strict field and
        expect ValidationError
        """
        check = lambda err:assertValidationError(err,[
            {'field':'id','errorType':'is_instance_of'}
        ])
        assert type(johnJson) == dict
        with pytest.raises(ValidationError,check=check):
            john = Person(**(johnJson|{"id":1234}))

    def test_update_forzen_field(self,johnJson:map):
        """
        Update frozen field and expect validation error
        """
        john = Person(**johnJson)
        #assert john.model_dump_json() == "{}"
        check = lambda err:assertValidationError(err,[
            {'field':'id','errorType':'frozen_field'}
        ])
        with pytest.raises(ValidationError,check=check):
            john.id = "1234" #frozen_field checking comes first before the strict field

    def test_age(self,johnJson:map):
        """
        """
        john = Person(**(johnJson|{"dob":"1989-06-04"}))
        assert john.dob == date(1989,6,4)
        assert john.age == (date.today() - date(1989,6,4)).days // 365.25
        