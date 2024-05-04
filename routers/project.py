from typing import List

from fastapi import APIRouter, Depends

from database import schemas, get_db, models, cruds
from helpers import TokenManager

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/get_by_user/{user_id}", response_model=List[schemas.ProjectOutput], dependencies=[Depends(get_db)])
async def get_user_projects(user_id: int, user: models.User | None = Depends(TokenManager.optionally_verify_token)):
    projects = cruds.get_projects_by_user(user_id)
    return [schemas.ProjectOutput(can_edit=user is not None and project.user_id == user, data=project.__data__) for
            project in projects]


@router.get("/get_by_id/{project_id}", response_model=schemas.ProjectOutput, dependencies=[Depends(get_db)])
async def get_project_by_id(project_id: int, user: models.User | None = Depends(TokenManager.optionally_verify_token)):
    project = cruds.get_project_by_id(project_id)
    return schemas.ProjectOutput(can_edit=user is not None and project.user_id == user, data=project.__data__)


@router.post("/create", response_model=schemas.ProjectOutput, dependencies=[Depends(get_db)])
async def create_project(project: schemas.ProjectCreate, user: models.User = Depends(TokenManager.verify_token)):
    project = cruds.create_project(user, project)
    return schemas.ProjectOutput(can_edit=True, data=project.__data__)
