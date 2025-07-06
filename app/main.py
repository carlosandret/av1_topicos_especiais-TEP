from fastapi import FastAPI, HTTPException, Query, Path, status
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

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
tasks_db = {}

@app.get("/tasks", response_model=List[Task], status_code=status.HTTP_200_OK)
def list_tasks(skip: int = Query(0, ge=0), limit: int = Query(10, gt=0)):
    """
    Lista tarefas com paginação via query string.
    """
    tasks = list(tasks_db.values())
    return tasks[skip: skip + limit]

@app.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def get_task(task_id: str = Path(...)):
    """
    Busca uma tarefa pelo ID via parâmetro de URL.
    """
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return task

@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    """
    Cria uma nova tarefa via corpo da requisição.
    """
    task_id = str(uuid4())
    new_task = Task(id=task_id, created_at=datetime.utcnow(), **task.dict())
    tasks_db[task_id] = new_task
    return new_task

@app.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task(task_id: str, task: TaskCreate):
    """
    Atualiza uma tarefa existente.
    """
    stored_task = tasks_db.get(task_id)
    if not stored_task:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    updated_task = Task(id=task_id, created_at=stored_task.created_at, **task.dict())
    tasks_db[task_id] = updated_task
    return updated_task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    """
    Remove uma tarefa.
    """
    if task_id in tasks_db:
        del tasks_db[task_id]
    else:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")