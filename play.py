from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# "Banco de dados" fake
usuarios = [
    {"id": 1, "username": "prof", "senha": "123", "tipo": "professor"},
    {"id": 2, "username": "aluno", "senha": "123", "tipo": "aluno"}
]

atividades = ["ABC123", "XYZ999"]

# =========================
# MODELOS
# =========================

class Login(BaseModel):
    username: str
    senha: str

class EntradaAtividade(BaseModel):
    codigo: str
    user_id: int

class CriarAtividade(BaseModel):
    codigo: str
    user_id: int

# =========================
# FUNÇÕES AUXILIARES
# =========================

def buscar_usuario_por_id(user_id):
    for user in usuarios:
        if user["id"] == user_id:
            return user
    return None

def verificar_professor(usuario):
    if usuario["tipo"] != "professor":
        raise HTTPException(status_code=403, detail="Acesso negado")

# =========================
# ROTAS
# =========================

@app.post("/login")
def login(dados: Login):
    for user in usuarios:
        if user["username"] == dados.username and user["senha"] == dados.senha:
            return {
                "mensagem": "Login sucesso",
                "usuario": {
                    "id": user["id"],
                    "tipo": user["tipo"]
                }
            }
    
    raise HTTPException(status_code=401, detail="Credenciais inválidas")


@app.post("/entrar-atividade")
def entrar_atividade(dados: EntradaAtividade):
    usuario = buscar_usuario_por_id(dados.user_id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if dados.codigo not in atividades:
        raise HTTPException(status_code=404, detail="Código inválido")

    return {
        "mensagem": "Entrada permitida",
        "usuario": usuario["username"],
        "tipo": usuario["tipo"]
    }


@app.post("/criar-atividade")
def criar_atividade(dados: CriarAtividade):
    usuario = buscar_usuario_por_id(dados.user_id)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    verificar_professor(usuario)

    atividades.append(dados.codigo)

    return {
        "mensagem": "Atividade criada com sucesso",
        "codigo": dados.codigo
    }

@app.get("/atividades")
def listar_atividades():
    return atividades