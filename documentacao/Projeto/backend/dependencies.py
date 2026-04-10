from fastapi import HTTPException
from backend.database import supabase


def verificar_professor(usuario_id: int):
    res = supabase.table("usuarios").select("tipo_usuario").eq("id", usuario_id).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if res.data["tipo_usuario"] not in ("professor", "admin"):
        raise HTTPException(status_code=403, detail="Acesso negado: apenas professores ou admin")


def verificar_admin(admin_id: int):
    res = supabase.table("adm").select("id").eq("id", admin_id).execute()
    if not res.data:
        raise HTTPException(status_code=403, detail="Acesso negado: apenas admin")