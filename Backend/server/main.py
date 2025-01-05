from fastapi import FastAPI
from routers import debug, function_call, help
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# routers
app.include_router(debug.app)
app.include_router(function_call.app)
app.include_router(help.app)


# cors policy
origins = [
    "http://localhost:6789",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)