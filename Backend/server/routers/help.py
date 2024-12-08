from fastapi import APIRouter
from fastapi import status
import random
from typing import Any
from contextlib import asynccontextmanager
import json

help_schema: list[Any] = []


@asynccontextmanager
async def lifespan(app: APIRouter):
    global help_schema

    with open("data/available_functions.json", 'r') as file:
        help_schema = json.load(file)
    yield
    return

app = APIRouter(prefix='/help', lifespan=lifespan)


@app.get('/get_number')
async def get_number_test():
    return {"result of help": random.randint(1, 144)}


@app.get('/', status_code=status.HTTP_200_OK)
async def get_schema() -> list[Any]:
    return help_schema
