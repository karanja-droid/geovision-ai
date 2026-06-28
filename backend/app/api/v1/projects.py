from fastapi import APIRouter, Depends
from typing import List, Optional
from pydantic import BaseModel

from backend.app.core.security import get_current_user

router = APIRouter()

class ProjectIn(BaseModel):
    name: str
    country: str = "Zambia"
    commodity: str = "Cu"
    description: Optional[str] = None

class ProjectOut(ProjectIn):
    id: int
    analyses_count: int = 0

_projects: dict[int, ProjectOut] = {}
_next_id = 1

@router.post("", response_model=ProjectOut)
async def create_project(p: ProjectIn, user: str = Depends(get_current_user)):
    global _next_id
    proj = ProjectOut(id=_next_id, **p.model_dump(), analyses_count=0)
    _projects[_next_id] = proj
    _next_id += 1
    return proj

@router.get("", response_model=List[ProjectOut])
async def list_projects(user: str = Depends(get_current_user)):
    if not _projects:
        _projects[0] = ProjectOut(id=0, name="Copperbelt Demo Project", country="Zambia", commodity="Cu", description="Pre-loaded demo", analyses_count=3)
    return list(_projects.values())

@router.get("/{project_id}", response_model=ProjectOut)
async def get_project(project_id: int, user: str = Depends(get_current_user)):
    return _projects.get(project_id, ProjectOut(id=project_id, name="Unknown", country="Zambia", commodity="Cu"))