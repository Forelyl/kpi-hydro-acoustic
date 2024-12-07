from fastapi import FastAPI
from routers import debug, function_call, help

app = FastAPI()

app.include_router(debug.app)
app.include_router(function_call.app)
app.include_router(help.app)
