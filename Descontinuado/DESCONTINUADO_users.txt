from fastapi import APIRouter, Depends, HTTPException
from backend.database import supabase
from backend.security import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/")
def listar_usuarios(
    current_user = Depends(get_current_user)
):

    usuarios = supabase.table("usuarios") \
        .select("id, nome, email, tipo_usuario") \
        .execute()

    return usuarios.data


@router.get("/{user_id}")
def buscar_usuario(
    user_id: int,
    current_user = Depends(get_current_user)
):

    usuario = supabase.table("usuarios") \
        .select("id, nome, email, tipo_usuario") \
        .eq("id", user_id) \
        .execute()

    if not usuario.data:

        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )

    return usuario.data[0]


@router.delete("/{user_id}")
def deletar_usuario(
    user_id: int,
    current_user = Depends(get_current_user)
):

    supabase.table("usuarios") \
        .delete() \
        .eq("id", user_id) \
        .execute()

    return {
        "mensagem": "Usuário deletado"
    }
