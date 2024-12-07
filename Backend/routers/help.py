from fastapi import APIRouter
import random

app = APIRouter(prefix='/help')


@app.get('/get_number')
async def a():
    return {"result of help": random.randint(1, 144)}
