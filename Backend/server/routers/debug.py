from fastapi import APIRouter, Response, status, UploadFile
import random
from threading import Thread

from functions.utils import play_audio


app = APIRouter(prefix='/debug')


@app.get('/get_number')
async def get_number_test():
    return {"result of debug": random.randint(1, 144)}


@app.post('/play_audio', status_code=status.HTTP_201_CREATED)
async def play_audio_test(file: UploadFile, response: Response):
    print(file.content_type)
    thread = Thread(target=play_audio, args=(file,))
    thread.start()

    return len(file.filename)
