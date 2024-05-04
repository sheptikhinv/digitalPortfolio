import datetime

import peewee

from ..database import db
from .. import models


class Comment(peewee.Model):
    user_id = peewee.ForeignKeyField(models.User, backref='comments', on_delete='CASCADE')
    project = peewee.ForeignKeyField(models.Project, backref='comments', on_delete='CASCADE')
    text = peewee.TextField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

