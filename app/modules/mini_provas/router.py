from fastapi import APIRouter, Depends
from .service import MiniProvaService
from .models import CorrecaoRequest
from uuid import UUID

router = APIRouter(prefix="/mini-provas", tags=["Mini-Provas"])
def get_mini_prova_service(): return MiniProvaService()

@router.get("/{prova_id}/iniciar/{usuario_id}")
def iniciar_prova(prova_id: UUID, usuario_id: int, service: MiniProvaService = Depends(get_mini_prova_service)):
    return service.iniciar_prova(prova_id, usuario_id)

@router.post("/corrigir")
def corrigir_prova(correcao: CorrecaoRequest, service: MiniProvaService = Depends(get_mini_prova_service)):
    return service.corrigir_prova(correcao)