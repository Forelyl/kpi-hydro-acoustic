from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import Annotated
import random
from pydantic import ValidationError
from functions.data_classes import Pipeline, Function_call
from functions.functions import make_pipeline
from functions.utils import pseudo_zip_result

app = APIRouter(prefix='/functions_call')


@app.get('/get_number')
async def get_number_test():
    return {"result of functions_call": random.randint(1, 144)}


# -----

async def pipeline_from_form(pipeline: Annotated[str, Form()]) -> Pipeline:
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
        pipeline: Annotated[str, Form()],
        separate: Annotated[bool, Form()]
):
    result = pseudo_zip_result()

    print(pipeline)
    return StreamingResponse(result, media_type="application/zip")
    result_zip = make_pipeline(file, pipeline, separate)
    return StreamingResponse(result_zip, media_type="application/zip")