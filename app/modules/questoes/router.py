from fastapi import APIRouter, Depends
from .service import QuestaoService
from .models import QuestaoCreate, QuestaoResponse
from typing import List
from uuid import UUID

router = APIRouter(prefix="/questoes", tags=["Questões"])
def get_questao_service(): return QuestaoService()

@router.post("/", response_model=dict)
def criar_questao(questao: QuestaoCreate, service: QuestaoService = Depends(get_questao_service)):
    return {"mensagem": "Questão cadastrada", "id": service.cadastrar(questao)}

@router.get("/", response_model=List[QuestaoResponse])
def listar_questoes(service: QuestaoService = Depends(get_questao_service)):
    return service.listar()

@router.get("/disciplina/{disciplina_id}")
def filtrar_disciplina(disciplina_id: UUID, service: QuestaoService = Depends(get_questao_service)):
    return service.filtrar_disciplina(disciplina_id)

@router.get("/dificuldade/{nivel}")
def filtrar_dificuldade(nivel: str, service: QuestaoService = Depends(get_questao_service)):
    return service.filtrar_nivel(nivel)