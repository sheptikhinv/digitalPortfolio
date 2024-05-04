import peewee

from ..database import db


class User(peewee.Model):
    # id = peewee.IntegerField(primary_key=True)
    email = peewee.CharField(unique=True, index=True)
    password = peewee.CharField()

    class Meta:
        database = db
