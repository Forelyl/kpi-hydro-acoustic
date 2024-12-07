from fastapi import APIRouter
import random

app = APIRouter(prefix='/function_call')


@app.get('/get_number')
async def a():
    return {"result of function_call": random.randint(1, 144)}
