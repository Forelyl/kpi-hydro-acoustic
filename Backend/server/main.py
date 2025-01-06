from fastapi import FastAPI
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