from fastapi import APIRouter, Depends, UploadFile
from starlette.responses import FileResponse

from database import schemas, models, cruds, get_db
from helpers import TokenManager, exceptions

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/{user_id}", response_model=schemas.ProfileResponse, dependencies=[Depends(get_db)])
async def get_profile_by_id(user_id: int, user: models.User | None = Depends(TokenManager.optionally_verify_token)):
    profile = cruds.get_profile_by_id(user_id)
    if profile is None:
        raise exceptions.profile_not_found
    return schemas.ProfileResponse(can_edit=user is not None and user.id == user_id,
                                   data=profile.to_dict())


@router.post("/create", response_model=schemas.ProfileResponse, dependencies=[Depends(get_db)])
async def create_profile(profile: schemas.ProfileCreate, user: models.User = Depends(TokenManager.verify_token)):
    profile = cruds.add_profile(user, profile)
    return schemas.ProfileResponse(can_edit=True, data=profile.to_dict())


@router.put("/update", response_model=schemas.ProfileResponse, dependencies=[Depends(get_db)])
async def update_profile(profile: schemas.ProfileUpdate, user: models.User = Depends(TokenManager.verify_token)):
    profile = cruds.update_profile(user, profile)
    return schemas.ProfileResponse(can_edit=True, data=profile.to_dict())


@router.post("/update_image")
async def update_image(file: UploadFile, user: models.User = Depends(TokenManager.verify_token)):
    if file.content_type not in ["image/png", "image/jpeg", "image/gif"]:
        raise exceptions.wrong_file_type
    return await cruds.update_profile_picture(user_id=user.id, file=file)


@router.get("/get_image/{user_id}", response_class=FileResponse)
async def get_image(user_id: int):
    return FileResponse(cruds.return_profile_picture(user_id))
