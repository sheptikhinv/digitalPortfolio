from fastapi import APIRouter, Depends

from database import schemas, models, cruds, get_db
from helpers import TokenManager

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/{user_id}", response_model=schemas.ProfileResponse, dependencies=[Depends(get_db)])
async def get_profile_by_id(user_id: int, user: models.User | None = Depends(TokenManager.optionally_verify_token)):
    profile = cruds.get_profile_by_id(user_id)
    print(profile.projects_count)
    print(profile.__dict__)
    return schemas.ProfileResponse(can_edit=user is not None and user.id == user_id,
                                   data=profile.__data__)


@router.post("/create", response_model=schemas.ProfileResponse, dependencies=[Depends(get_db)])
async def create_profile(profile: schemas.ProfileCreate, user: models.User = Depends(TokenManager.verify_token)):
    profile = cruds.add_profile(user, profile)
    return schemas.ProfileResponse(can_edit=True, data=profile.__data__)


@router.put("/update", response_model=schemas.ProfileResponse, dependencies=[Depends(get_db)])
async def update_profile(profile: schemas.ProfileUpdate, user: models.User = Depends(TokenManager.verify_token)):
    profile = cruds.update_profile(user, profile)
    return schemas.ProfileResponse(can_edit=True, data=profile.__data__)
