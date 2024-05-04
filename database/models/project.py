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
    def likes_count(self) -> int:
        likes = self.likes.count()
        self.__data__['likes_count'] = likes
        return likes

    @property
    def comments_count(self) -> int:
        comments = self.comments.count()
        self.__data__['comments_count'] = comments
        return comments

    @property
    def project_images(self):
        return [image.image_path for image in self.images]

    class Meta:
        database = db

