import os
from typing import List

from fastapi import UploadFile
from peewee import IntegrityError

from database import models, schemas
from helpers import exceptions


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


def subscribe_profile(author_id: int, subscriber: models.User) -> models.Subscription:
    author = models.User.get_by_id(author_id)
    if author is None:
        raise exceptions.user_not_found
    subscription = models.Subscription.select().where(
        (models.Subscription.author == author) & (models.Subscription.subscriber == subscriber)).exists()
    print(f"Is subscription exists for {author_id} by {subscriber.id}: {subscription}")
    if not subscription:
        print(f"Создаем subscription author_id: {author_id} subscriber_id: {subscriber.id}")
        subscription = models.Subscription(author=author, subscriber=subscriber)
        subscription.save()
        print(subscription)
    return author


def unsubscribe_from_profile(author_id: int, subscriber: models.User):
    author = models.User.get_by_id(author_id)
    if author is None:
        raise exceptions.user_not_found

    try:
        subscription = models.Subscription.select().where(
            (models.Subscription.author == author) & (models.Subscription.subscriber == subscriber)).get()
        subscription.delete_instance()
    except models.Subscription.DoesNotExist:
        ...
    return author


def get_subscriptions(subscriber: models.User) -> List[models.Profile]:
    subscriptions = models.Subscription.filter(models.Subscription.subscriber == subscriber)
    return [get_profile_by_id(subscription.author.id) for subscription in subscriptions]
