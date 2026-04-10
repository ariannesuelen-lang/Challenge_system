from fastapi import APIRouter, HTTPException
from backend.database import supabase
from backend.models import VotoCreate

router = APIRouter()


@router.post("/votos")
def votar(dados: VotoCreate):
    existe = supabase.table("votos").select("id").eq("resposta_id", dados.resposta_id).eq("usuario_id", dados.usuario_id).execute()
    if existe.data:
        raise HTTPException(status_code=409, detail="Você já votou nesta resposta")
    res = supabase.table("votos").insert({
        "resposta_id": dados.resposta_id,
        "usuario_id": dados.usuario_id
    }).execute()
    return {"mensagem": "Voto registrado com sucesso", "voto": res.data[0]}


@router.delete("/votos")
def remover_voto(resposta_id: int, usuario_id: int):
    res = supabase.table("votos").delete().eq("resposta_id", resposta_id).eq("usuario_id", usuario_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Voto não encontrado")
    return {"mensagem": "Voto removido com sucesso"}