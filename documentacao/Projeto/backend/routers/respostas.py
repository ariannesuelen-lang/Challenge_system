from fastapi import APIRouter
from backend.database import supabase
from backend.models import RespostaCreate

router = APIRouter()


@router.get("/desafios/{desafio_id}/respostas")
def listar_respostas(desafio_id: int):
    res = supabase.table("respostas").select("*, usuarios(nome), votos(id)").eq("desafio_id", desafio_id).execute()
    result = []
    for r in res.data:
        r["usuario_nome"] = r.pop("usuarios", {}).get("nome", "")
        r["total_votos"] = len(r.pop("votos", []))
        result.append(r)
    result.sort(key=lambda x: x["total_votos"], reverse=True)
    return result


@router.post("/respostas")
def criar_resposta(dados: RespostaCreate):
    res = supabase.table("respostas").insert({
        "desafio_id": dados.desafio_id,
        "usuario_id": dados.usuario_id,
        "conteudo": dados.conteudo
    }).execute()
    return {"mensagem": "Resposta enviada com sucesso", "resposta": res.data[0]}