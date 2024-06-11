from typing import List

from fastapi import APIRouter, Depends, UploadFile
from starlette import status
from starlette.responses import FileResponse

from database import schemas, models, cruds, get_db
from helpers import TokenManager, exceptions, mappers

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/subscriptions", response_model=List[schemas.ProfileResponse], dependencies=[Depends(get_db)])
async def get_subscriptions(user: models.User = Depends(TokenManager.verify_token)):
    return [mappers.profile_to_output(user=user, profile=profile) for profile in cruds.get_subscriptions(user)]


@router.get("/{user_id}", response_model=schemas.ProfileResponse, dependencies=[Depends(get_db)])
async def get_profile_by_id(user_id: int, user: models.User | None = Depends(TokenManager.optionally_verify_token)):
    profile = cruds.get_profile_by_id(user_id)
    if profile is None:
        raise exceptions.profile_not_found
    return mappers.profile_to_output(user, profile)


@router.post("/create", response_model=schemas.ProfileResponse, dependencies=[Depends(get_db)])
async def create_profile(profile: schemas.ProfileCreate, user: models.User = Depends(TokenManager.verify_token)):
    profile = cruds.add_profile(user, profile)
    return mappers.profile_to_output(user, profile)


@router.put("/update", response_model=schemas.ProfileResponse, dependencies=[Depends(get_db)])
async def update_profile(profile: schemas.ProfileUpdate, user: models.User = Depends(TokenManager.verify_token)):
    profile = cruds.update_profile(user, profile)
    return mappers.profile_to_output(user, profile)


@router.post("/update_image")
async def update_image(file: UploadFile, user: models.User = Depends(TokenManager.verify_token)):
    if file.content_type not in ["image/png", "image/jpeg", "image/gif"]:
        raise exceptions.wrong_file_type
    return await cruds.update_profile_picture(user_id=user.id, file=file)


@router.get("/get_image/{user_id}", response_class=FileResponse)
async def get_image(user_id: int):
    return FileResponse(cruds.return_profile_picture(user_id))


@router.post("/subscribe/{user_id}", response_model=schemas.ProfileResponse, dependencies=[Depends(get_db)])
async def subscribe_profile(user_id: int, user: models.User = Depends(TokenManager.verify_token)):
    if user_id == user.id:
        raise exceptions.subscribed_to_yourself
    author = cruds.subscribe_profile(author_id=user_id, subscriber=user)
    profile = cruds.get_profile_by_id(user_id=user_id)
    return mappers.profile_to_output(user=user, profile=profile)


@router.delete("/unsubscribe/{user_id}", response_model=schemas.ProfileResponse, dependencies=[Depends(get_db)])
async def unsubscribe_profile(user_id: int, user: models.User = Depends(TokenManager.verify_token)):
    author = cruds.unsubscribe_from_profile(author_id=user_id, subscriber=user)
    profile = cruds.get_profile_by_id(user_id=user_id)
    return mappers.profile_to_output(user=user, profile=profile)
