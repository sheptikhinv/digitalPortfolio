from datetime import timedelta, datetime

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from starlette import status

from database import cruds, models
from . import exceptions
from .config import get_value

security = HTTPBearer(auto_error=False)


class TokenManager:
    secret_key = get_value("SECRET_KEY")

    @classmethod
    def create_token(cls, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=6)
        to_encode.update({"exp": expire})
        encoded_token = jwt.encode(to_encode, cls.secret_key, algorithm="HS256")
        return encoded_token

    @classmethod
    def verify_token(cls, credentials: HTTPAuthorizationCredentials = Depends(security)) -> models.User:
        if not credentials:
            raise exceptions.credentials_exception

        token = credentials.credentials
        try:
            payload = jwt.decode(token, cls.secret_key, algorithms="HS256")
            user_id = payload.get("sub")
            if user_id is None:
                raise exceptions.credentials_exception
            user = cruds.get_user_by_id(user_id)
            if user is None:
                raise exceptions.credentials_exception
            return user
        except JWTError as e:
            raise exceptions.credentials_exception

    @classmethod
    def optionally_verify_token(cls, credentials: HTTPAuthorizationCredentials = Depends(security,
                                                                                         use_cache=False)) -> models.User | None:
        if not credentials:
            return None

        try:
            return cls.verify_token(credentials)

        except HTTPException as e:
            return None
