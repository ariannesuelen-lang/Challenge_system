from fastapi import APIRouter, HTTPException
from typing import Optional
from backend.database import supabase
from backend.models import DesafioCreate, DesafioUpdate
from backend.dependencies import verificar_professor

router = APIRouter()


@router.get("/desafios")
def listar_desafios(disciplina_id: Optional[int] = None):
    query = supabase.table("desafios").select("*, usuarios(nome), disciplinas(nome)")
    if disciplina_id:
        query = query.eq("disciplina_id", disciplina_id)
    res = query.order("data_criacao", desc=True).execute()
    result = []
    for d in res.data:
        d["criador_nome"] = d.pop("usuarios", {}).get("nome", "")
        d["disciplina_nome"] = d.pop("disciplinas", {}).get("nome", "") if d.get("disciplinas") else ""
        result.append(d)
    return result


@router.get("/desafios/{desafio_id}")
def buscar_desafio(desafio_id: int):
    res = supabase.table("desafios").select("*, usuarios(nome), disciplinas(nome)").eq("id", desafio_id).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    d = res.data
    d["criador_nome"] = d.pop("usuarios", {}).get("nome", "")
    d["disciplina_nome"] = d.pop("disciplinas", {}).get("nome", "") if d.get("disciplinas") else ""
    return d


@router.post("/desafios")
def criar_desafio(dados: DesafioCreate):
    verificar_professor(dados.criador_id)
    res = supabase.table("desafios").insert({
        "titulo": dados.titulo,
        "descricao": dados.descricao,
        "criador_id": dados.criador_id,
        "disciplina_id": dados.disciplina_id,
        "data_limite": dados.data_limite
    }).execute()
    return {"mensagem": "Desafio criado com sucesso", "desafio": res.data[0]}


@router.put("/desafios/{desafio_id}")
def atualizar_desafio(desafio_id: int, dados: DesafioUpdate, usuario_id: int):
    verificar_professor(usuario_id)
    res = supabase.table("desafios").update({
        "titulo": dados.titulo,
        "descricao": dados.descricao,
        "disciplina_id": dados.disciplina_id,
        "data_limite": dados.data_limite
    }).eq("id", desafio_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    return {"mensagem": "Desafio atualizado com sucesso", "desafio": res.data[0]}


@router.delete("/desafios/{desafio_id}")
def deletar_desafio(desafio_id: int, usuario_id: int):
    verificar_professor(usuario_id)
    res = supabase.table("desafios").delete().eq("id", desafio_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    return {"mensagem": "Desafio deletado com sucesso"}