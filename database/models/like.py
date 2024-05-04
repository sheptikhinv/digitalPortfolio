import datetime

import peewee

from ..database import db
from .. import models


class Like(peewee.Model):
    user_id = peewee.ForeignKeyField(models.User, backref='likes', on_delete='CASCADE')
    project = peewee.ForeignKeyField(models.Project, backref='likes', on_delete='CASCADE')
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

