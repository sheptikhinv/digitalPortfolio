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
        return projects_count

    @property
    def subscribers_count(self):
        subscribers_count = models.Subscription.select().where(models.Subscription.author == self.user_id).count()
        return subscribers_count

    def to_dict(self):
        result = self.__data__
        result.update(projects_count=self.projects_count, subscribers_count=self.subscribers_count)
        return result

    def is_subscribed(self, user: models.User) -> bool:
        return models.Subscription.select().where(
            (models.Subscription.author == self.user_id) & (models.Subscription.subscriber == user)
        ).exists()

    class Meta:
        database = db
