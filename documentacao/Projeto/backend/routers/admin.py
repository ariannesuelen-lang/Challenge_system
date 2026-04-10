from fastapi import APIRouter, HTTPException
from backend.database import supabase
from backend.dependencies import verificar_admin
from backend.models import UsuarioTipoUpdate

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/usuarios")
def listar_usuarios(admin_id: int):
    verificar_admin(admin_id)
    res = supabase.table("usuarios").select("id, nome, email, tipo_usuario").order("nome").execute()
    return res.data


@router.put("/usuarios/{usuario_id}/tipo")
def alterar_tipo_usuario(usuario_id: int, dados: UsuarioTipoUpdate, admin_id: int):
    verificar_admin(admin_id)
    if dados.novo_tipo not in ("aluno", "professor"):
        raise HTTPException(status_code=400, detail="Tipo inválido. Use 'aluno' ou 'professor'")
    res = supabase.table("usuarios").update({"tipo_usuario": dados.novo_tipo}).eq("id", usuario_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"mensagem": "Tipo atualizado com sucesso", "usuario": res.data[0]}


@router.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int, admin_id: int):
    verificar_admin(admin_id)
    res = supabase.table("usuarios").delete().eq("id", usuario_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"mensagem": "Usuário deletado com sucesso"}


@router.delete("/desafios/{desafio_id}")
def deletar_desafio_admin(desafio_id: int, admin_id: int):
    verificar_admin(admin_id)
    res = supabase.table("desafios").delete().eq("id", desafio_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    return {"mensagem": "Desafio deletado com sucesso"}


@router.delete("/respostas/{resposta_id}")
def deletar_resposta_admin(resposta_id: int, admin_id: int):
    verificar_admin(admin_id)
    res = supabase.table("respostas").delete().eq("id", resposta_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")  # ← corrigido
    return {"mensagem": "Resposta deletada com sucesso"}


@router.post("/cursos")
def criar_curso_admin(admin_id: int, nome: str):
    verificar_admin(admin_id)
    res = supabase.table("cursos").insert({"nome": nome}).execute()
    return res.data[0]


@router.delete("/cursos/{curso_id}")
def deletar_curso_admin(curso_id: int, admin_id: int):
    verificar_admin(admin_id)
    res = supabase.table("cursos").delete().eq("id", curso_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return {"mensagem": "Curso deletado com sucesso"}


@router.post("/disciplinas")
def criar_disciplina_admin(admin_id: int, nome: str, curso_id: int):
    verificar_admin(admin_id)
    res = supabase.table("disciplinas").insert({"nome": nome, "curso_id": curso_id}).execute()
    return res.data[0]


@router.delete("/disciplinas/{disciplina_id}")
def deletar_disciplina_admin(disciplina_id: int, admin_id: int):
    verificar_admin(admin_id)
    res = supabase.table("disciplinas").delete().eq("id", disciplina_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
    return {"mensagem": "Disciplina deletada com sucesso"}