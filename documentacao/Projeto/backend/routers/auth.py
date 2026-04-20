from fastapi import APIRouter, HTTPException
from backend.database import supabase
from backend.models import LoginInput, UsuarioCreate
from backend.security import hash_senha, verificar_senha

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(dados: LoginInput):
    res = supabase.table("usuarios").select("*").eq("email", dados.email).execute()
    if not res.data:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    usuario = res.data[0]

    if not verificar_senha(dados.senha, usuario["senha"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    usuario.pop("senha", None)

    return{
        "mensagem": "Login realizado com sucesso",
        "usuario": usuario
    }


@router.post("/usuarios")
def criar_usuario(dados: UsuarioCreate):
    existe = supabase.table("usuarios").select("id").eq("email", dados.email).execute()
    if existe.data:
        raise HTTPException(status_code=409, detail="Email já cadastrado")
    senha_hash = hash_senha(dados.senha)
    res = supabase.table("usuarios").insert({
        "nome": dados.nome,
        "email": dados.email,
        "senha": senha_hash,
        "tipo_usuario": dados.tipo_usuario
    }).execute()
    usuario = res.data[0]
    usuario.pop("senha", None)

    return {
        "mensagem": "Usuário criado com sucesso", 
        "usuario": usuario
    }
