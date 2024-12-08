from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
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


async def pipeline_from_form(pipeline: Annotated[str, Form()]) -> Pipeline:
    print(pipeline)
    # return Pipeline(pipeline=[{"id": 1, "track": [1], "args": [1, 2]}])
    try:
        return Pipeline.model_validate_json(pipeline, strict=True)
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail=e.errors(include_url=False, include_context=False)
        )


@app.post('/', status_code=status.HTTP_200_OK, response_class=StreamingResponse)
async def pipeline_interface(
        file:     Annotated[UploadFile, File()],
        pipeline: Annotated[Pipeline, Depends(pipeline_from_form)],
        separate: Annotated[bool, Form()]
):
    def iterfile():
        with open("server/temp_data/zip_example.zip", mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(), media_type="application/zip")