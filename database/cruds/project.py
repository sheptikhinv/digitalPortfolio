import base64
import datetime
import uuid
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


def get_subscribed_projects(offset: int, limit: int, user: models.User) -> List[models.Project]:
    return (models.Project.
            select()
            .where(models.Project.user_id << [subscription.author for subscription in user.subscriptions])
            .offset(offset)
            .limit(limit))


def add_image_to_project(project: models.Project, image: schemas.ProjectImage) -> models.Project:
    image_uuid = str(uuid.uuid4())
    image_data = image.picture.split(",")
    image_bytes = str.encode(image_data[1])
    file_format = image_data[0].split('/')[1].split(';')[0]
    with open(f"img/{image_uuid}.{file_format}", "wb") as file:
        file.write(base64.urlsafe_b64decode(image_bytes))
    project_image = models.ProjectImage(project=project, picture=f"{image_uuid}.{file_format}",
                                        description=image.description)
    project_image.save()
    return project


def add_preview(preview: str) -> str:
    image_uuid = str(uuid.uuid4())
    image_data = preview.split(",")
    image_bytes = str.encode(image_data[1])
    file_format = image_data[0].split('/')[1].split(';')[0]
    with open(f"img/{image_uuid}.{file_format}", "wb") as file:
        file.write(base64.urlsafe_b64decode(image_bytes))
    return f"{image_uuid}.{file_format}"


def delete_image_from_project(project: models.Project) -> bool:
    ...


def get_project_image(path: str):
    return f"img/{path}"


def create_project(user: models.User, project: schemas.ProjectCreate) -> models.Project:
    project_db = models.Project(user_id=user, title=project.title, description=project.description)
    project_db.preview = add_preview(project.preview)
    project_db.save()
    for image in project.pictures:
        add_image_to_project(project_db, image)
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
