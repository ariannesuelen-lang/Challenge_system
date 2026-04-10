from fastapi import APIRouter
from backend.database import supabase
from backend.models import CursoCreate

router = APIRouter()


@router.get("/cursos")
def listar_cursos():
    res = supabase.table("cursos").select("*").order("nome").execute()
    return res.data


@router.post("/cursos")
def criar_curso(dados: CursoCreate):
    res = supabase.table("cursos").insert({"nome": dados.nome}).execute()
    return res.data[0]