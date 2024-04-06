from database import models, schemas
from helpers import PasswordManager


def get_user_by_id(user_id: int) -> models.User:
    return models.User.filter(models.User.id == user_id).first()


def get_user_by_email(email: str) -> models.User:
    return models.User.filter(models.User.email == email).first()


def add_user(user: schemas.UserInput) -> models.User:
    user_db = models.User(email=user.email, password=PasswordManager.get_password_hash(user.password))
    user_db.save()
    return user_db
