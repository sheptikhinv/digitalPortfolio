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
