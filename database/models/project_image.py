import peewee

from ..database import db
from .. import models


class ProjectImage(peewee.Model):
    project = peewee.ForeignKeyField(models.Project, backref='images', on_delete='CASCADE')
    image_path = peewee.CharField(unique=True, null=False)

    class Meta:
        database = db

