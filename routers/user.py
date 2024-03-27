from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from database import schemas, cruds, get_db, models
from helpers import TokenManager, PasswordManager

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.Token, dependencies=[Depends(get_db)])
async def create_user(user: schemas.UserCreate):
    user_db = cruds.add_user(user)
    return schemas.Token(access_token=TokenManager.create_token(data={"sub": str(user_db.id)}), token_type="bearer")


@router.post("/login", response_model=schemas.Token, dependencies=[Depends(get_db)])
async def login_user(user: schemas.UserAuthenticate):
    user_db = cruds.get_user_by_email(user.email)
    if not user_db or not PasswordManager.verify_password(user.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    return schemas.Token(access_token=TokenManager.create_token(data={"sub": str(user_db.id)}), token_type="bearer")


@router.get("/me", response_model=schemas.UserBase, dependencies=[Depends(get_db)])
async def current_user(user: models.User = Depends(TokenManager.verify_token)):
    return user
