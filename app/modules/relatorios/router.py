from fastapi import APIRouter
from core.database import Database

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

@router.get("/diarios")
def listar_resultados_diarios():
    return Database().get_client().table("resultados_diarios_mini_provas").select("*").execute().data