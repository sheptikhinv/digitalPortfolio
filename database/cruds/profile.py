import os

from fastapi import UploadFile
from peewee import IntegrityError

from database import models, schemas


def get_profile_by_id(user_id: int) -> models.Profile:
    return models.Profile.filter(models.Profile.user_id == user_id).first()


def add_profile(user: models.User, profile: schemas.ProfileCreate) -> models.Profile:
    profile_db = models.Profile(user_id=user, **profile.dict())
    try:
        profile_db.save()
    except IntegrityError:
        return update_profile(user, profile)
    return profile_db


def update_profile(user: models.User, profile: schemas.ProfileUpdate) -> models.Profile:
    profile_db = get_profile_by_id(user.id)
    profile_dict = profile.dict()
    for key, value in profile_dict.items():
        setattr(profile_db, key, value)
    profile_db.save()
    return profile_db


async def update_profile_picture(user_id: int, file: UploadFile) -> bool:
    filenames = [f for f in os.listdir("img") if f.startswith(f'{user_id}.')]
    for filename in filenames:
        os.remove(f"img/{filename}")
    with open(f"img/{user_id}.{file.filename.split('.')[1]}", "wb") as f:
        f.write(await file.read())
    return True


def return_profile_picture(user_id: int) -> str:
    filenames = [f for f in os.listdir("img") if f.startswith(f'{user_id}.')]
    if filenames:
        return f"img/{filenames[0]}"
    return "img/default.png"
