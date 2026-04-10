from fastapi import APIRouter, HTTPException
from backend.database import supabase
from backend.models import LoginInput, UsuarioCreate

router = APIRouter()


@router.post("/login")
def login(dados: LoginInput):
    # Tenta login como admin primeiro (tabela separada e segura)
    adm = supabase.table("adm").select("id, nome, email").eq("email", dados.email).eq("senha", dados.senha).execute()
    if adm.data:
        usuario = adm.data[0]
        usuario["tipo_usuario"] = "admin"
        return {"mensagem": "Login realizado com sucesso", "usuario": usuario}

    # Login comum
    res = supabase.table("usuarios").select("id, nome, email, tipo_usuario").eq("email", dados.email).eq("senha", dados.senha).execute()
    if not res.data:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"mensagem": "Login realizado com sucesso", "usuario": res.data[0]}


@router.post("/usuarios")
def criar_usuario(dados: UsuarioCreate):
    # Impede cadastro como admin pela rota pública
    if dados.tipo_usuario == "admin":
        raise HTTPException(status_code=403, detail="Tipo de usuário inválido")
    existe = supabase.table("usuarios").select("id").eq("email", dados.email).execute()
    if existe.data:
        raise HTTPException(status_code=409, detail="Email já cadastrado")
    res = supabase.table("usuarios").insert({
        "nome": dados.nome,
        "email": dados.email,
        "senha": dados.senha,
        "tipo_usuario": dados.tipo_usuario
    }).execute()
    return {"mensagem": "Usuário criado com sucesso", "usuario": res.data[0]}