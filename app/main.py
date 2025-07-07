from fastapi import FastAPI, HTTPException, Query, Path, status
from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from app.schemas.schemas import Message, ProjectSchema, ProjectPublic, ProjectDB

from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class Task(TaskCreate):
    id: str
    created_at: datetime

app = FastAPI(
    title="API de Tarefas",
    description="API para gestão de tarefas a fazer",
    version="0.1.0"
)

# Simulação de banco de dados em memória
# tasks_db = {}
projects_bd = []

# Criação do andPoint da home

@app.get("/", response_model=Message, status_code=status.HTTP_200_OK)
def read_root():
    return {'message': 'Olá mundo!'}

# Criação de um novo projeto
@app.post("/projects", response_model=ProjectPublic , status_code=status.HTTP_201_CREATED) 
def create_project(project: ProjectSchema):
    
    project_with_id = ProjectDB(
        id = len(projects_bd) +1,
        **project.model_dump()
    )
    projects_bd.append(project_with_id)
    return project_with_id

# Listar todos os projetos por paginação
@app.get("/projects", response_model=ProjectDB, status_code=status.HTTP_200_OK)
def read_projects(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0)):
    projects = List(projects_bd.values())
    return projects[skip: skip + limit]
    
# @app.get("/projects", status_code=status.HTTP_200_OK)
# def read_projects():
#     return {'projects': projects_bd}

# Atualizar um projeto existente
@app.put("/projects/{project_id}",response_model=ProjectPublic, status_code=status.HTTP_200_OK)
# Vai atualizar os dados que foram recebidos originalmente
def update_project(project_id: int, project: ProjectSchema):
    project_with_id = ProjectDB(        
        **project.model_dump(),
        id = project_id)
    projects_bd[project_id - 1] = project_with_id
    
    return project_with_id 

# Busca um projeto especifico  pelo id 
@app.get("/projects/{project_id}", response_model=ProjectDB, status_code=status.HTTP_200_OK)
def get_project(project_id: str = Path(...)):
    project = projects_bd.get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Projeto não foi encontrado")
    return project

# Deletar um projeto

@app.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: str):
    if project_id in projects_bd:
        del project_id[project_id]
    else:
        raise HTTPException(status_code=404, detail="Projeto não foi encontrado")
    