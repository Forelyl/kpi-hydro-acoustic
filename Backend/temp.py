from pydantic import Field, field_validator, ValidationError, RootModel
from pydantic import ValidationInfo
from pydantic import BaseModel
from typing import Annotated, Any, ClassVar
from enum import Enum


class Time(BaseModel):
    minutes: Annotated[int, Field(ge=0)]
    seconds: Annotated[int, Field(ge=0, lt=60)]


class Track_characteristic(str, Enum):
    Frequency = "frequency"
    Amplitude = "amplitude"
    Time      = "time"


POSITIVE_INT_CHECK       = RootModel[Annotated[int, Field(gt=0)]]
FLOAT_CHECK              = RootModel[float]
POSITIVE_FLOAT_CHECK     = RootModel[Annotated[float, Field(gt=0.0)]]
NON_NEGATIVE_FLOAT_CHECK = RootModel[Annotated[float, Field(ge=0.0)]]
TIME_CHECK               = RootModel[Time]
TRACK_CHECK              = RootModel[list[Annotated[int, Field(ge=0)]]]
TRACK_CHARACTER_CHECK    = RootModel[Track_characteristic]


class A(BaseModel):
    id: Annotated[int, Field(ge=0, le=2)]
    a: list[Any]

    # ---
    __INT_CHECK: ClassVar[RootModel] = RootModel[int]

    __ARGS_TYPES: ClassVar[tuple[tuple[type]]] = (
        (__INT_CHECK,),
        (FLOAT_CHECK, FLOAT_CHECK),
        (TIME_CHECK,),
    )

    # ---

    @field_validator("a")
    @classmethod
    def __check_trait(cls, a: list[Any], b: ValidationInfo) -> list[int | float | Time | Track_characteristic]:
        checkers: tuple[type] = A.__ARGS_TYPES[b.data["id"]]
        if len(checkers) != len(a):
            raise ValueError("Wrong number of arguments")
        for i in range(len(checkers)):
            a[i] = checkers[i].model_validate(a[i]).root
        return a


try:
    obj_a = A(a=[1,], id=0)
    print("Valid:", obj_a)

    obj_b = A(a=[2.2, 3], id=1)
    print("Valid:", obj_b)

    obj_c = A(a=[{"minutes": 1, "seconds": 0}], id=2)
    print("Valid:", obj_c)
except ValidationError as e:
    print("Error:", e.json())

for i in range(12, 15):
    print('*' * i)