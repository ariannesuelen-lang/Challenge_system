from pydantic import BaseModel
from typing import Optional


class LoginInput(BaseModel):
    email: str
    senha: str


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    tipo_usuario: str


class DesafioCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    criador_id: int
    criador_tipo: str  # "professor" ou "admin"
    disciplina_id: Optional[int] = None
    data_limite: Optional[str] = None


class DesafioUpdate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    disciplina_id: Optional[int] = None
    data_limite: Optional[str] = None


class RespostaCreate(BaseModel):
    desafio_id: int
    usuario_id: int
    usuario_tipo: str  # "aluno", "professor" ou "admin"
    conteudo: str


class VotoCreate(BaseModel):
    resposta_id: int
    usuario_id: int


class CursoCreate(BaseModel):
    nome: str


class DisciplinaCreate(BaseModel):
    nome: str
    curso_id: int


class UsuarioTipoUpdate(BaseModel):
    novo_tipo: str  # "aluno" ou "professor"