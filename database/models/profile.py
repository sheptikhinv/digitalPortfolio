import peewee

from ..database import db
from .. import models


class Profile(peewee.Model):
    user_id = peewee.ForeignKeyField(models.User, unique=True, backref="profile")
    name = peewee.CharField()
    education = peewee.CharField(null=True)
    description = peewee.TextField(null=True)
    phone_number = peewee.CharField(null=True)
    email = peewee.CharField(null=True)

    @property
    def projects_count(self):
        projects_count = models.Project.select().where(models.Project.user_id == self.user_id).count()
        self.__data__['projects_count'] = projects_count
        return projects_count

    class Meta:
        database = db
