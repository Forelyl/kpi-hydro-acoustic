from fastapi import FastAPI, Request
from routers import debug, function_call, help
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
import sys
from datetime import datetime
from functions.functions import Audio_track


# runtime context manager
@asynccontextmanager
async def app_lifecycle_context(app: FastAPI):
    is_debug: bool = "--reload" in sys.argv
    Audio_track.set_use_function(is_debug)

    # Start info
    print("=" * 30)
    print("Starting application...")
    print("Time:", datetime.now())
    print("Debug:", is_debug)
    print("=" * 30)

    yield

    return

# FastAPI main object
app = FastAPI(lifespan=app_lifecycle_context)

# routers
app.include_router(debug.app)
app.include_router(function_call.app)
app.include_router(help.app)


# cors policy
origins = [
    "http://localhost:6789",
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    content_type = request.headers.get("content-type")
    print(f"Content-Type: {content_type}")  # This shows the body type (e.g., application/json)
    print(f"Request Method: {request.method}")
    print(f"Request URL: {request.url}")
    body = await request.body()  # Read the request body
    # print(f"Request Body: {body}")
    response = await call_next(request)
    return response
