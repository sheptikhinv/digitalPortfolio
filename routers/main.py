from fastapi import FastAPI

from helpers.config import get_value
from .user import router as user_router
from .profile import router as profile_router
from .project import router as project_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

is_development = get_value("is_development")

if is_development.lower() in ["true", "yes", "y"]:
    origins = [
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000"
        "http://localhost",
        "http://localhost:3000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(user_router)
app.include_router(profile_router)
app.include_router(project_router)
