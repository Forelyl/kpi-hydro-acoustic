from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from typing import Annotated
import random
from pydantic import BaseModel, ValidationError

app = APIRouter(prefix='/functions_call')


@app.get('/get_number')
async def get_number_test():
    return {"result of functions_call": random.randint(1, 144)}


class Function_call(BaseModel):
    id:    int
    track: list[int] | None = None
    args:  list


class Pipeline(BaseModel):
    pipeline: list[Function_call]


async def pipeline_deserialize(pipeline: Annotated[str, Form()]) -> Pipeline:
    print(pipeline)
    # return Pipeline(pipeline=[{"id": 1, "track": [1], "args": [1, 2]}])
    try:
        return Pipeline.model_validate_json(pipeline)
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=e.errors()
        )
    # try:
    # except ValueError as e:
    #     print(e)
    #     return None
    # await input("...")
    # return Pipeline.model_validate(pipeline)


class A(BaseModel):
    a: int
    b: int

#   Invalid JSON: expected value at line 1 column 1 [type=json_invalid, input_value='string', input_type=str]
#     For further information visit https://errors.pydantic.dev/2.10/v/json_invalid


@app.post('/')
async def pipeline_interface(
        file: Annotated[UploadFile, File()],
        pipeline: Annotated[Pipeline, Depends(pipeline_deserialize)],
):
    # print("Pipe:", pipeline)
    return