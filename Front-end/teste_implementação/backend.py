from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# SUPABASE
# =========================

supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# =========================
# MODELOS
# =========================

class LoginInput(BaseModel):
    email: str
    senha: str

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    tipo_usuario: str

class UsuarioUpdate(BaseModel):
    nome: str
    email: str
    senha: Optional[str] = None
    tipo_usuario: str

class DesafioCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    criador_id: int
    disciplina_id: Optional[int] = None
    data_limite: Optional[str] = None

class DesafioUpdate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    disciplina_id: Optional[int] = None
    data_limite: Optional[str] = None

class RespostaCreate(BaseModel):
    desafio_id: int
    usuario_id: int
    conteudo: str

class VotoCreate(BaseModel):
    resposta_id: int
    usuario_id: int

class CursoCreate(BaseModel):
    nome: str

class DisciplinaCreate(BaseModel):
    nome: str
    curso_id: int

# =========================
# FUNÇÕES AUXILIARES
# =========================

def verificar_professor(usuario_id: int):
    res = supabase.table("usuarios").select("tipo_usuario").eq("id", usuario_id).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    if res.data["tipo_usuario"] != "professor":
        raise HTTPException(status_code=403, detail="Acesso negado: apenas professores")

# =========================
# ROTAS - AUTH
# =========================

@app.post("/login")
def login(dados: LoginInput):
    res = supabase.table("usuarios").select("id, nome, email, tipo_usuario").eq("email", dados.email).eq("senha", dados.senha).execute()
    if not res.data:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {"mensagem": "Login realizado com sucesso", "usuario": res.data[0]}

@app.post("/usuarios")
def criar_usuario(dados: UsuarioCreate):
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

@app.get("/usuarios/{usuario_id}")
def buscar_usuario(usuario_id: int):
    res = supabase.table("usuarios").select("id, nome, email, tipo_usuario").eq("id", usuario_id).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return res.data

@app.put("/usuarios/{usuario_id}")
def atualizar_usuario(usuario_id: int, dados: UsuarioUpdate):
    existe = supabase.table("usuarios").select("id").eq("email", dados.email).neq("id", usuario_id).execute()
    if existe.data:
        raise HTTPException(status_code=409, detail="Este email já está em uso por outro usuário")

    payload = {
        "nome": dados.nome,
        "email": dados.email,
        "tipo_usuario": dados.tipo_usuario
    }
    if dados.senha:
        payload["senha"] = dados.senha

    res = supabase.table("usuarios").update(payload).eq("id", usuario_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"mensagem": "Usuário atualizado com sucesso", "usuario": res.data[0]}

# =========================
# ROTAS - CURSOS
# =========================

@app.get("/cursos")
def listar_cursos():
    res = supabase.table("cursos").select("*").order("nome").execute()
    return res.data

@app.post("/cursos")
def criar_curso(dados: CursoCreate):
    res = supabase.table("cursos").insert({"nome": dados.nome}).execute()
    return res.data[0]

# =========================
# ROTAS - DISCIPLINAS
# =========================

@app.get("/disciplinas")
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

@app.post("/disciplinas")
def criar_disciplina(dados: DisciplinaCreate):
    res = supabase.table("disciplinas").insert({
        "nome": dados.nome,
        "curso_id": dados.curso_id
    }).execute()
    return res.data[0]

# =========================
# ROTAS - DESAFIOS
# =========================

@app.get("/desafios")
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

@app.get("/desafios/{desafio_id}")
def buscar_desafio(desafio_id: int):
    res = supabase.table("desafios").select("*, usuarios(nome), disciplinas(nome)").eq("id", desafio_id).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    d = res.data
    d["criador_nome"] = d.pop("usuarios", {}).get("nome", "")
    d["disciplina_nome"] = d.pop("disciplinas", {}).get("nome", "") if d.get("disciplinas") else ""
    return d

@app.post("/desafios")
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

@app.put("/desafios/{desafio_id}")
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

@app.delete("/desafios/{desafio_id}")
def deletar_desafio(desafio_id: int, usuario_id: int):
    verificar_professor(usuario_id)
    res = supabase.table("desafios").delete().eq("id", desafio_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Desafio não encontrado")
    return {"mensagem": "Desafio deletado com sucesso"}

# =========================
# ROTAS - RESPOSTAS
# =========================

@app.get("/desafios/{desafio_id}/respostas")
def listar_respostas(desafio_id: int):
    res = supabase.table("respostas").select("*, usuarios(nome), votos(id)").eq("desafio_id", desafio_id).execute()
    result = []
    for r in res.data:
        r["usuario_nome"] = r.pop("usuarios", {}).get("nome", "")
        r["total_votos"] = len(r.pop("votos", []))
        result.append(r)
    result.sort(key=lambda x: x["total_votos"], reverse=True)
    return result

@app.post("/respostas")
def criar_resposta(dados: RespostaCreate):
    res = supabase.table("respostas").insert({
        "desafio_id": dados.desafio_id,
        "usuario_id": dados.usuario_id,
        "conteudo": dados.conteudo
    }).execute()
    return {"mensagem": "Resposta enviada com sucesso", "resposta": res.data[0]}

# =========================
# ROTAS - VOTOS
# =========================

@app.post("/votos")
def votar(dados: VotoCreate):
    existe = supabase.table("votos").select("id").eq("resposta_id", dados.resposta_id).eq("usuario_id", dados.usuario_id).execute()
    if existe.data:
        raise HTTPException(status_code=409, detail="Você já votou nesta resposta")
    res = supabase.table("votos").insert({
        "resposta_id": dados.resposta_id,
        "usuario_id": dados.usuario_id
    }).execute()
    return {"mensagem": "Voto registrado com sucesso", "voto": res.data[0]}

@app.delete("/votos")
def remover_voto(resposta_id: int, usuario_id: int):
    res = supabase.table("votos").delete().eq("resposta_id", resposta_id).eq("usuario_id", usuario_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Voto não encontrado")
    return {"mensagem": "Voto removido com sucesso"}

# =========================
# ROTAS - ADMIN
# =========================

@app.get("/admin/usuarios")
def listar_usuarios_admin():
    res = supabase.table("usuarios").select("id, nome, email, tipo_usuario").order("nome").execute()
    return res.data

@app.delete("/admin/usuarios/{usuario_id}")
def deletar_usuario_admin(usuario_id: int):
    res = supabase.table("usuarios").delete().eq("id", usuario_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"mensagem": "Usuário removido com sucesso"}

@app.delete("/admin/desafios/{desafio_id}")
def deletar_desafio_admin(desafio_id: int):
    res = supabase.table("desafios").delete().eq("id", desafio_id).execute()
    return {"mensagem": "Desafio removido"}

@app.delete("/admin/cursos/{curso_id}")
def deletar_curso_admin(curso_id: int):
    res = supabase.table("cursos").delete().eq("id", curso_id).execute()
    return {"mensagem": "Curso removido"}

@app.delete("/admin/disciplinas/{disciplina_id}")
def deletar_disciplina_admin(disciplina_id: int):
    res = supabase.table("disciplinas").delete().eq("id", disciplina_id).execute()
    return {"mensagem": "Disciplina removida"}

@app.delete("/admin/respostas/{resposta_id}")
def deletar_resposta_admin(resposta_id: int):
    res = supabase.table("respostas").delete().eq("id", resposta_id).execute()
    return {"mensagem": "Resposta removida"}