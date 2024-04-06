import peewee

from ..database import db
from .. import models


class Profile(peewee.Model):
    user_id = peewee.ForeignKeyField(models.User, unique=True)
    name = peewee.CharField()
    education = peewee.CharField(null=True)
    description = peewee.TextField(null=True)
    phone_number = peewee.CharField(null=True)
    email = peewee.CharField(null=True)

    class Meta:
        database = db
