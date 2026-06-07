from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    tipo_usuario: str  # 'aluno' ou 'professor'
    matricula: Optional[str] = None
    turma: Optional[str] = None

class UsuarioResponse(BaseModel):
    id: int
    usuario_uuid: UUID
    nome: str
    email: str
    tipo_usuario: str
    matricula: Optional[str]
    turma: Optional[str]
    ativo: bool