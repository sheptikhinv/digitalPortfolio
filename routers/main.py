from fastapi import FastAPI
from .user import router as user_router
from .profile import router as profile_router

app = FastAPI()

app.include_router(user_router)
app.include_router(profile_router)
