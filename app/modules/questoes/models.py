from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

class AlternativaCreate(BaseModel):
    texto: str
    correta: bool
    ordem_exibicao: int

class QuestaoCreate(BaseModel):
    professor_id: UUID 
    disciplina_id: UUID
    tema_id: Optional[UUID] = None
    tipo_questao: str = "multipla_escolha"
    nivel_dificuldade: str  
    enunciado: str
    explicacao: Optional[str] = None
    pontos: float = 1.00
    alternativas: List[AlternativaCreate]

class AlternativaResponse(BaseModel):
    id: UUID
    texto: str
    correta: bool
    ordem_exibicao: int

class QuestaoResponse(BaseModel):
    id: UUID
    professor_id: UUID
    disciplina_id: UUID
    tema_id: Optional[UUID]
    tipo_questao: str
    nivel_dificuldade: str
    enunciado: str
    explicacao: Optional[str]
    pontos: float
    ativo: bool
    alternativas: List[AlternativaResponse] = []