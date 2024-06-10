import datetime
from typing import List

import peewee

from database import models, schemas
from helpers import exceptions


def get_project_by_id(project_id: int) -> models.Project:
    return models.Project.filter(models.Project.id == project_id).first()


def get_projects_by_user(user_id: int) -> List[models.Project]:
    return models.Project.filter(models.Project.user_id == user_id)


def get_projects(offset: int, limit: int) -> List[models.Project]:
    return models.Project.select().offset(offset).limit(limit)


def get_newest_projects(offset: int, limit: int) -> List[models.Project]:
    return models.Project.select().order_by(models.Project.created_at.desc()).offset(offset).limit(limit)


def create_project(user: models.User, project: schemas.ProjectCreate) -> models.Project:
    project_db = models.Project(user_id=user, **project.dict())
    project_db.save()
    return project_db


def update_project(user_id: int, project: schemas.ProjectUpdate, project_id: int) -> models.Project:
    project_db = models.Project.filter(models.Project.id == project_id and models.Project.user_id == user_id).first()
    project_dict = project.dict()
    for key, value in project_dict.items():
        setattr(project_db, key, value)
    project_db.save()
    return project_db


def delete_project(user_id: int, project_id: int) -> bool:
    project_db = models.Project.filter(models.Project.id == project_id and models.Project.user_id == user_id).first()
    project_db.delete_instance()
    return True


def add_image_to_project(user: models.User) -> models.Project:
    ...


def delete_image_from_project(user: models.User) -> bool:
    ...


def add_like_to_project(user: models.User, project_id: int) -> models.Project:
    project = get_project_by_id(project_id)
    if project is None:
        raise exceptions.project_not_found
    like = models.Like.select().where(models.Like.user_id == user and models.Like.project_id == project_id).exists()
    if not like:
        like = models.Like(user_id=user, project_id=project)
        like.save()
    return project


def delete_like_from_project(user: models.User, project_id: int) -> models.Project:
    project = get_project_by_id(project_id)
    if project is None:
        raise exceptions.project_not_found

    try:
        like = models.Like.select().where(models.Like.user_id == user and models.Like.project_id == project_id).get()
        like.delete_instance()
    except models.Like.DoesNotExist:
        ...

    return project


def add_comment_to_project(user: models.User, project_id: int, comment: schemas.CommentCreate) -> models.Comment:
    project = get_project_by_id(project_id)
    if project is None:
        raise Exception("Project not found")
    comment_db = models.Comment(user_id=user, project_id=project,
                                created_at=datetime.datetime.now(), **comment.dict())
    comment_db.save()
    return comment_db


def delete_comment_from_project(user: models.User) -> bool:
    ...
