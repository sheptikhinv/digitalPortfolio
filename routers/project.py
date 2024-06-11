from typing import List

from fastapi import APIRouter, Depends

from database import schemas, get_db, models, cruds
from helpers import TokenManager, exceptions, mappers

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/get_by_user/{user_id}", response_model=List[schemas.ProjectOutput], dependencies=[Depends(get_db)])
async def get_user_projects(user_id: int, user: models.User | None = Depends(TokenManager.optionally_verify_token)):
    projects = cruds.get_projects_by_user(user_id)
    return [mappers.project_to_output(user=user, project=project) for
            project in projects]


@router.get("/get_by_id/{project_id}", response_model=schemas.ProjectOutput, dependencies=[Depends(get_db)])
async def get_project_by_id(project_id: int, user: models.User | None = Depends(TokenManager.optionally_verify_token)):
    project = cruds.get_project_by_id(project_id)
    if project is None:
        raise exceptions.project_not_found
    return mappers.project_to_output(user=user, project=project)


@router.post("/create", response_model=schemas.ProjectOutput, dependencies=[Depends(get_db)])
async def create_project(project: schemas.ProjectCreate, user: models.User = Depends(TokenManager.verify_token)):
    project = cruds.create_project(user, project)
    return mappers.project_to_output(user=user, project=project)


@router.get("/all", response_model=List[schemas.ProjectOutput], dependencies=[Depends(get_db)])
async def get_projects(limit: int = 10, offset: int = 0,
                       user: models.User = Depends(TokenManager.optionally_verify_token)):
    projects = cruds.get_projects(offset=offset, limit=limit)
    return [mappers.project_to_output(user=user, project=project) for project in projects]


@router.get("/newest", response_model=List[schemas.ProjectOutput], dependencies=[Depends(get_db)])
async def get_newest_projects(limit: int = 10, offset: int = 0,
                              user: models.User = Depends(TokenManager.optionally_verify_token)):
    projects = cruds.get_newest_projects(offset=offset, limit=limit)
    return [mappers.project_to_output(user=user, project=project) for project in projects]


@router.get("/subscribed", response_model=List[schemas.ProjectOutput], dependencies=[Depends(get_db)])
async def get_subscribed_projects(limit: int = 10, offset: int = 0,
                                  user: models.User = Depends(TokenManager.verify_token)):
    projects = cruds.get_subscribed_projects(offset=offset, limit=limit, user=user)
    return [mappers.project_to_output(user=user, project=project) for project in projects]


@router.post("/add_like", response_model=schemas.ProjectOutput, dependencies=[Depends(get_db)])
async def like_project(project_id: int, user: models.User = Depends(TokenManager.verify_token)):
    project = cruds.add_like_to_project(user=user, project_id=project_id)
    return mappers.project_to_output(user=user, project=project)


@router.delete("/delete_like", response_model=schemas.ProjectOutput, dependencies=[Depends(get_db)])
async def unlike_project(project_id: int, user: models.User = Depends(TokenManager.verify_token)):
    project = cruds.delete_like_from_project(user=user, project_id=project_id)
    return mappers.project_to_output(user=user, project=project)
