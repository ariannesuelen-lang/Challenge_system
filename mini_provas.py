# =========================================================
# SISTEMA DE MINI-PROVAS
# FASTAPI + SQLITE + FIREBASE
# =========================================================
#
# INSTALAÇÃO:
#
# pip install fastapi uvicorn firebase-admin
#
# EXECUTAR:
#
# uvicorn app:app --reload
#
# DOCUMENTAÇÃO AUTOMÁTICA:
#
# http://127.0.0.1:8000/docs
#
# =========================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
import random
from datetime import datetime

# =========================================================
# FIREBASE
# =========================================================

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred)

firebase_db = firestore.client()

# =========================================================
# FASTAPI
# =========================================================

app = FastAPI(
    title="API Mini-Provas",
    description="Sistema de mini-provas rápidas",
    version="1.0"
)

# =========================================================
# BANCO SQLITE
# =========================================================

def conectar():

    conn = sqlite3.connect("mini_provas.db")

    conn.row_factory = sqlite3.Row

    return conn

# =========================================================
# CRIAÇÃO DAS TABELAS
# =========================================================

conn = conectar()
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS questoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    disciplina TEXT,
    tema TEXT,
    dificuldade TEXT,
    pergunta TEXT,
    alternativa_a TEXT,
    alternativa_b TEXT,
    alternativa_c TEXT,
    alternativa_d TEXT,
    resposta_correta TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS resultados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER,
    nota INTEGER,
    acertos INTEGER,
    erros INTEGER,
    data TEXT
)
""")

conn.commit()
conn.close()

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
# CADASTRAR ALUNO
# =========================================================

@app.post("/alunos")
def cadastrar_aluno(aluno: Aluno):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO alunos (nome)
    VALUES (?)
    """, (aluno.nome,))

    conn.commit()

    aluno_id = cursor.lastrowid

    conn.close()

    # =====================================================
    # FIREBASE
    # =====================================================

    firebase_db.collection("alunos").document(str(aluno_id)).set({
        "nome": aluno.nome,
        "dataCadastro": datetime.now().strftime("%d/%m/%Y")
    })

    return {
        "mensagem": "Aluno cadastrado com sucesso",
        "id": aluno_id
    }

# =========================================================
# LISTAR ALUNOS
# =========================================================

@app.get("/alunos")
def listar_alunos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM alunos")

    alunos = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return alunos

# =========================================================
# CADASTRAR QUESTÃO
# =========================================================

@app.post("/questoes")
def cadastrar_questao(questao: Questao):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO questoes (
        disciplina,
        tema,
        dificuldade,
        pergunta,
        alternativa_a,
        alternativa_b,
        alternativa_c,
        alternativa_d,
        resposta_correta
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        questao.disciplina,
        questao.tema,
        questao.dificuldade,
        questao.pergunta,
        questao.alternativa_a,
        questao.alternativa_b,
        questao.alternativa_c,
        questao.alternativa_d,
        questao.resposta_correta
    ))

    conn.commit()

    questao_id = cursor.lastrowid

    conn.close()

    # =====================================================
    # FIREBASE
    # =====================================================

    firebase_db.collection("questoes").document(str(questao_id)).set({
        "disciplina": questao.disciplina,
        "tema": questao.tema,
        "dificuldade": questao.dificuldade,
        "pergunta": questao.pergunta
    })

    return {
        "mensagem": "Questão cadastrada",
        "id": questao_id
    }

# =========================================================
# LISTAR QUESTÕES
# =========================================================

@app.get("/questoes")
def listar_questoes():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questoes")

    questoes = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return questoes

# =========================================================
# INICIAR MINI PROVA
# =========================================================

@app.get("/mini-prova/{aluno_id}")
def iniciar_mini_prova(aluno_id: int):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questoes")

    questoes = cursor.fetchall()

    if len(questoes) < 5:

        raise HTTPException(
            status_code=400,
            detail="Necessário no mínimo 5 questões"
        )

    # =====================================================
    # RANDOMIZAÇÃO DAS QUESTÕES
    # =====================================================

    sorteadas = random.sample(questoes, 5)

    mini_prova = []

    for q in sorteadas:

        alternativas = [
            q["alternativa_a"],
            q["alternativa_b"],
            q["alternativa_c"],
            q["alternativa_d"]
        ]

        # =================================================
        # RANDOMIZAÇÃO DAS ALTERNATIVAS
        # =================================================

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

    conn.close()

    return {

        "aluno_id": aluno_id,

        "duracao_total": "5 minutos",

        "quantidade_questoes": 5,

        "questoes": mini_prova
    }

# =========================================================
# CORRIGIR PROVA
# =========================================================

@app.post("/corrigir")
def corrigir_prova(correcao: Correcao):

    conn = conectar()
    cursor = conn.cursor()

    acertos = 0
    erros = 0

    topicos_fracos = []

    for resposta in correcao.respostas:

        cursor.execute("""
        SELECT * FROM questoes
        WHERE id = ?
        """, (resposta.questao_id,))

        questao = cursor.fetchone()

        if not questao:
            continue

        correta = questao["resposta_correta"]

        if resposta.resposta == correta:

            acertos += 1

        else:

            erros += 1

            topicos_fracos.append({
                "disciplina": questao["disciplina"],
                "tema": questao["tema"]
            })

    nota = acertos * 2

    # =====================================================
    # SALVAR RESULTADO SQLITE
    # =====================================================

    cursor.execute("""
    INSERT INTO resultados (
        aluno_id,
        nota,
        acertos,
        erros,
        data
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        correcao.aluno_id,
        nota,
        acertos,
        erros,
        datetime.now().strftime("%d/%m/%Y")
    ))

    conn.commit()

    resultado_id = cursor.lastrowid

    conn.close()

    # =====================================================
    # SALVAR FIREBASE
    # =====================================================

    firebase_db.collection("resultados").document(str(resultado_id)).set({

        "aluno_id": correcao.aluno_id,

        "nota": nota,
        "acertos": acertos,
        "erros": erros,

        "topicos_fracos": topicos_fracos,

        "data": datetime.now().strftime("%d/%m/%Y")
    })

    return {

        "nota": nota,
        "acertos": acertos,
        "erros": erros,

        "topicos_fracos": topicos_fracos
    }

# =========================================================
# RELATÓRIOS
# =========================================================

@app.get("/relatorios")
def relatorios():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        alunos.nome,
        resultados.nota,
        resultados.acertos,
        resultados.erros,
        resultados.data
    FROM resultados
    JOIN alunos
    ON alunos.id = resultados.aluno_id
    """)

    resultados = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return resultados

# =========================================================
# RANKING
# =========================================================

@app.get("/ranking")
def ranking():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        alunos.nome,
        AVG(resultados.nota) as media
    FROM resultados
    JOIN alunos
    ON alunos.id = resultados.aluno_id
    GROUP BY alunos.id
    ORDER BY media DESC
    """)

    ranking = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return ranking

# =========================================================
# FILTRO POR DISCIPLINA
# =========================================================

@app.get("/questoes/disciplina/{disciplina}")
def filtrar_disciplina(disciplina: str):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM questoes
    WHERE disciplina = ?
    """, (disciplina,))

    questoes = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return questoes

# =========================================================
# FILTRO POR DIFICULDADE
# =========================================================

@app.get("/questoes/dificuldade/{dificuldade}")
def filtrar_dificuldade(dificuldade: str):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM questoes
    WHERE dificuldade = ?
    """, (dificuldade,))

    questoes = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return questoes