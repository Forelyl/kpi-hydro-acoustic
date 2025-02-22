from pydantic import BaseModel, field_validator, Field, ValidationInfo, RootModel, model_validator
from typing import Annotated, Any, ClassVar


class Time(BaseModel):
    minutes: Annotated[int, Field(ge=0)]
    seconds: Annotated[int, Field(ge=0, lt=60)]


class Function_call(BaseModel):
    __MIN_ID: ClassVar[int] = 0
    __MAX_ID: ClassVar[int] = 11

    # ---

    f_id:  Annotated[int, Field(ge=__MIN_ID, le=__MAX_ID)]   # should be before track and args for validation
    track: list[int]                   # should be after f_id for validation
    args:  list                        # should be after f_id for validation

    # ---

    __USE_EXPLICIT_TRACK: ClassVar[tuple[bool]] = (        # f_id is a position (counting from 0)
        True,  # 00
        True,  # 01
        True,  # 02
        True,  # 03
        True,  # 04
        True,  # 05
        True,  # 06
        True,  # 07
        True,  # 08
        True,  # 09
        True,  # 10
        True,  # 11
    )

    @model_validator(mode='before')
    @classmethod
    def validate_f_id_first(cls, values: dict[str, Any]) -> dict[str, Any]:
        f_id = values.get("f_id")
        if f_id is None or not (cls.__MIN_ID <= f_id <= cls.__MAX_ID):
            raise ValueError("Invalid f_id")
        return values

    @field_validator("track")
    @classmethod
    def __check_tracks(cls, tracks: list[int] | None, info: ValidationInfo):
        use_explicit = tracks is not None
        if cls.__USE_EXPLICIT_TRACK[info.data["f_id"]] != use_explicit:
            if cls.__USE_EXPLICIT_TRACK[info.data["f_id"]]:
                raise ValueError("Input track is unspecified")
            else:
                raise ValueError("Input track is specified, yet shouldn't be such")

        for i in range(len(tracks)): # TODO: try to add check on correct id
            if tracks[i] <= 0:
                raise ValueError("Input track is incorrect, 0 or less")
            tracks[i] -= 1

        return tracks

    # ---

    __INT_CHECK                : ClassVar[RootModel] = RootModel[int]
    __POSITIVE_INT_CHECK       : ClassVar[RootModel] = RootModel[Annotated[int, Field(gt=0)]]
    __FLOAT_CHECK              : ClassVar[RootModel] = RootModel[float]
    __POSITIVE_FLOAT_CHECK     : ClassVar[RootModel] = RootModel[Annotated[float, Field(gt=0.0)]]
    __NON_NEGATIVE_FLOAT_CHECK : ClassVar[RootModel] = RootModel[Annotated[float, Field(ge=0.0)]]
    __TIME_CHECK               : ClassVar[RootModel] = RootModel[Time]
    __TRACK_CHECK              : ClassVar[RootModel] = RootModel[list[Annotated[int, Field(ge=0)]]]

    __FUNCTIONS_ARGS: ClassVar[tuple[tuple[type]]] = (  # id is a position (counting from 0)
        (__POSITIVE_FLOAT_CHECK,),                                                      # 00
        (__POSITIVE_FLOAT_CHECK,),                                                      # 01
        (__POSITIVE_FLOAT_CHECK, __POSITIVE_FLOAT_CHECK),                               # 02
        (__POSITIVE_FLOAT_CHECK, __POSITIVE_FLOAT_CHECK),                               # 03
        (__FLOAT_CHECK,),                                                               # 04
        (__NON_NEGATIVE_FLOAT_CHECK,),                                                  # 05
        (),                                                                             # 06
        (__FLOAT_CHECK,),                                                               # 07
        (__TIME_CHECK, __TIME_CHECK),                                                   # 08
        (),                                                                             # 09
        (),                                                                             # 10
        (__POSITIVE_INT_CHECK,)                                                         # 11
    )

    @field_validator("args")
    @classmethod
    def __check_trait(cls, args: list[Any], validated_info: ValidationInfo) -> list[int | float | Time]:
        checkers: tuple[type] = cls.__FUNCTIONS_ARGS[validated_info.data["f_id"]]
        if len(checkers) != len(args):
            raise ValueError("Wrong number of arguments")
        for i in range(len(checkers)):
            args[i] = checkers[i].model_validate(args[i]).root
        return args

    # ---


class Pipeline(BaseModel):
    pipeline: list[Function_call]
