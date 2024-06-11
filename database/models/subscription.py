import datetime

import peewee

from ..database import db
from .. import models


class Subscription(peewee.Model):
    subscriber = peewee.ForeignKeyField(models.User, backref='subscriptions', on_delete='CASCADE')
    author = peewee.ForeignKeyField(models.User, backref='subscribers', on_delete='CASCADE')
    created_at = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
