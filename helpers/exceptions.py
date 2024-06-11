from fastapi import HTTPException
from starlette import status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

profile_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Profile not found"
)

project_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Project not found"
)

wrong_file_type = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Cant process this file here"
)

user_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)

subscribed_to_yourself = HTTPException(
    status_code=status.HTTP_406_NOT_ACCEPTABLE,
    detail="Subscirbing to yourself"
)
