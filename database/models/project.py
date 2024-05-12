import datetime

import peewee

from ..database import db
from .. import models


class Project(peewee.Model):
    user_id = peewee.ForeignKeyField(models.User, backref='projects')
    title = peewee.CharField()
    description = peewee.TextField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    @property
    def profile(self) -> models.Profile:
        return self.user_id.profile.get()

    @property
    def username(self) -> str:
        return self.profile.name

    @property
    def likes_count(self) -> int:
        return self.likes.count()

    @property
    def comments_count(self) -> int:
        return self.comments.count()

    @property
    def project_images(self):
        return [image.image_path for image in self.images]

    def to_dict(self):
        result = self.__data__
        result.update(username=self.username, likes_count=self.likes_count, comments_count=self.comments_count,
                      project_images=self.project_images)
        return result

    def is_liked(self, user: models.User) -> bool:
        return models.Like.select().where(
            (models.Like.user_id == user) & (models.Like.project == self)
        ).exists()

    class Meta:
        database = db
