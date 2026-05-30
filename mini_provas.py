# =========================================================
# SISTEMA DE MINI-PROVAS
# FASTAPI + SUPABASE
# =========================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import random
from datetime import datetime

# =========================================================
# SUPABASE
# =========================================================

from supabase import create_client, Client

SUPABASE_URL = "https://SEU_PROJETO.supabase.co"
SUPABASE_KEY = "SUA_SERVICE_ROLE_KEY"

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =========================================================
# FASTAPI
# =========================================================

app = FastAPI(
    title="API Mini-Provas",
    description="Sistema de mini-provas rápidas",
    version="2.0"
)

# =========================================================
# MODELS
# =========================================================

class Aluno(BaseModel):
    nome: str

class Questao(BaseModel):
    disciplina: str
    tema: str
    dificuldade: str
    pergunta: str
    alternativa_a: str
    alternativa_b: str
    alternativa_c: str
    alternativa_d: str
    resposta_correta: str

class RespostaItem(BaseModel):
    questao_id: int
    resposta: str

class Correcao(BaseModel):
    aluno_id: int
    respostas: List[RespostaItem]

# =========================================================
# ALUNOS
# =========================================================

@app.post("/alunos")
def cadastrar_aluno(aluno: Aluno):

    result = supabase.table("alunos").insert({
        "nome": aluno.nome
    }).execute()

    return {
        "mensagem": "Aluno cadastrado",
        "id": result.data[0]["id"]
    }

@app.get("/alunos")
def listar_alunos():

    result = supabase.table("alunos").select("*").execute()
    return result.data

# =========================================================
# QUESTÕES
# =========================================================

@app.post("/questoes")
def cadastrar_questao(questao: Questao):

    result = supabase.table("questoes").insert({
        "disciplina": questao.disciplina,
        "tema": questao.tema,
        "dificuldade": questao.dificuldade,
        "pergunta": questao.pergunta,
        "alternativa_a": questao.alternativa_a,
        "alternativa_b": questao.alternativa_b,
        "alternativa_c": questao.alternativa_c,
        "alternativa_d": questao.alternativa_d,
        "resposta_correta": questao.resposta_correta
    }).execute()

    return {
        "mensagem": "Questão cadastrada",
        "id": result.data[0]["id"]
    }

@app.get("/questoes")
def listar_questoes():

    result = supabase.table("questoes").select("*").execute()
    return result.data

# =========================================================
# MINI PROVA
# =========================================================

@app.get("/mini-prova/{aluno_id}")
def iniciar_mini_prova(aluno_id: int):

    result = supabase.table("questoes").select("*").execute()
    questoes = result.data

    if len(questoes) < 5:
        raise HTTPException(
            status_code=400,
            detail="Necessário no mínimo 5 questões"
        )

    sorteadas = random.sample(questoes, 5)

    mini_prova = []

    for q in sorteadas:

        alternativas = [
            q["alternativa_a"],
            q["alternativa_b"],
            q["alternativa_c"],
            q["alternativa_d"]
        ]

        random.shuffle(alternativas)

        mini_prova.append({
            "id": q["id"],
            "disciplina": q["disciplina"],
            "tema": q["tema"],
            "dificuldade": q["dificuldade"],
            "pergunta": q["pergunta"],
            "alternativas": alternativas,
            "tempo_maximo_questao": "60 segundos"
        })

    return {
        "aluno_id": aluno_id,
        "duracao_total": "5 minutos",
        "quantidade_questoes": 5,
        "questoes": mini_prova
    }

# =========================================================
# CORREÇÃO
# =========================================================

@app.post("/corrigir")
def corrigir_prova(correcao: Correcao):

    acertos = 0
    erros = 0
    topicos_fracos = []

    for resposta in correcao.respostas:

        result = supabase.table("questoes") \
            .select("*") \
            .eq("id", resposta.questao_id) \
            .execute()

        if not result.data:
            continue

        questao = result.data[0]

        if resposta.resposta == questao["resposta_correta"]:
            acertos += 1
        else:
            erros += 1
            topicos_fracos.append({
                "disciplina": questao["disciplina"],
                "tema": questao["tema"]
            })

    nota = acertos * 2

    supabase.table("resultados").insert({
        "aluno_id": correcao.aluno_id,
        "nota": nota,
        "acertos": acertos,
        "erros": erros
    }).execute()

    return {
        "nota": nota,
        "acertos": acertos,
        "erros": erros,
        "topicos_fracos": topicos_fracos
    }

# =========================================================
# RELATÓRIOS (VIEW)
# =========================================================

@app.get("/relatorios")
def relatorios():

    result = supabase.table("relatorios").select("*").execute()
    return result.data

# =========================================================
# RANKING (VIEW)
# =========================================================

@app.get("/ranking")
def ranking():

    result = supabase.table("ranking").select("*").execute()
    return result.data

# =========================================================
# FILTROS
# =========================================================

@app.get("/questoes/disciplina/{disciplina}")
def filtrar_disciplina(disciplina: str):

    result = supabase.table("questoes") \
        .select("*") \
        .eq("disciplina", disciplina) \
        .execute()

    return result.data


@app.get("/questoes/dificuldade/{dificuldade}")
def filtrar_dificuldade(dificuldade: str):

    result = supabase.table("questoes") \
        .select("*") \
        .eq("dificuldade", dificuldade) \
        .execute()

    return result.data
