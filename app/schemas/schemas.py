from typing import Any, Literal, Optional
from pydantic import BaseModel

class Message(BaseModel):
    message: str
    
class ProjectSchema(BaseModel):
    titulo: str
    descricao: str
    status: Literal['Planejado', 'Em Andamento', 'Concluído', 'Cancelado']
    prioridade: Literal[1, 2, 3]
    
class ProjectDB(ProjectSchema):
    id: int

# Retorna o projeto criado com elementos a mais ou a menos
class ProjectPublic(BaseModel):
    id: int
    titulo: str
    descricao: str
    status: Literal['Planejado', 'Em Andamento', 'Concluído', 'Cancelado']
    prioridade: Literal[1, 2, 3]
    
