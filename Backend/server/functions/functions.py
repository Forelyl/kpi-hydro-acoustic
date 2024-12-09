from functions.data_classes import Pipeline # , Function_call, Track_characteristic, Time
from fastapi import UploadFile
from io import BytesIO
from functions.utils import pseudo_zip_result


def make_pipeline(track: UploadFile, pipeline: Pipeline, to_separate_track: bool) -> BytesIO:
    return pseudo_zip_result()