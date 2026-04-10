from fastapi import APIRouter
from typing import Optional
from backend.database import supabase
from backend.models import DisciplinaCreate

router = APIRouter()


@router.get("/disciplinas")
def listar_disciplinas(curso_id: Optional[int] = None):
    query = supabase.table("disciplinas").select("*, cursos(nome)")
    if curso_id:
        query = query.eq("curso_id", curso_id)
    res = query.order("nome").execute()
    result = []
    for d in res.data:
        d["curso_nome"] = d.pop("cursos", {}).get("nome", "")
        result.append(d)
    return result


@router.post("/disciplinas")
def criar_disciplina(dados: DisciplinaCreate):
    res = supabase.table("disciplinas").insert({
        "nome": dados.nome,
        "curso_id": dados.curso_id
    }).execute()
    return res.data[0]