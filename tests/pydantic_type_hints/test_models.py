import pytest
import pydantic
from pydantic_type_hints.models import SimpleModel

def test_not_work_for_property_assignment():
    "Convertion is not apply for property assignment"
    # String could convert to int with the constructor
    testee = SimpleModel(intField="1")
    assert isinstance(testee.intField,int)
    # But convertion does not apply for property assignment
    testee.intField = "2.0"
    with pytest.raises(AssertionError):
        assert isinstance(testee.intField,int)


@pytest.mark.parametrize("intValue",[
    (1),("1"),(bytes(b"1")),(1.0),(0xF),(0b1),(0o7)])
def test_int_convertion(intValue:int):
    "Value pass into SimpleModel.intField should convert into int type"
    testee = SimpleModel(intField=intValue)
    assert isinstance(testee.intField,int),"SimpleModel.intField should be int type"

class TestSimpleModel:
    @pytest.mark.parametrize("intValue",[
        (1.1),(bytearray(b'1')),("abcd"),(b'not_a_int')
    ])
    def test_int_convert_fail(self,intValue:int):
        "Values fail to convert to Simple.intField"
        with pytest.raises(pydantic.ValidationError,match="intField"):
            testee = SimpleModel(intField=intValue)