# =========================================================
# SISTEMA DE MINI-PROVAS (ATUALIZADO COM NOVO SCRIPT SQL)
# FASTAPI + SUPABASE
# =========================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random
from uuid import UUID
import os
from dotenv import load_dotenv

load_dotenv()

# =========================================================
# SUPABASE CONFIGURAÇÃO
# =========================================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

from supabase import create_client, Client

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="API Mini-Provas v2",
    description="Sistema de mini-provas rápidas adaptado ao novo Schema do Banco",
    version="2.0"
)

# =========================================================
# MODELS (PYDANTIC)
# =========================================================

class AlunoCadastro(BaseModel):
    nome: str
    email: str
    matricula: Optional[str] = None
    turma: Optional[str] = None

class QuestaoCadastro(BaseModel):
    professor_id: UUID
    disciplina_id: UUID
    tema_id: Optional[UUID] = None
    nivel: str  # Deve ser: 'facil', 'intermediario' ou 'dificil'
    enunciado: str
    explicacao: Optional[str] = None
    pontos: float = 1.00
    alternativas: List[str]  # Lista contendo os textos das 4 alternativas
    index_correta: int      # Índice (0 a 3) indicando qual posição da lista é a correta

class RespostaItem(BaseModel):
    questao_id: UUID
    alternativa_id: UUID

class Correcao(BaseModel):
    tentativa_id: UUID
    respostas: List[RespostaItem]

# =========================================================
# ROTAS: ALUNOS
# =========================================================

@app.post("/alunos")
def cadastrar_aluno(aluno: AlunoCadastro):
    try:
        result = supabase.table("alunos").insert({
            "nome": aluno.nome,
            "email": aluno.email,
            "matricula": aluno.matricula,
            "turma": aluno.turma
        }).execute()

        return {
            "mensagem": "Aluno cadastrado com sucesso",
            "id": result.data[0]["id"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/alunos")
def listar_alunos():
    result = supabase.table("alunos").select("*").execute()
    return result.data

# =========================================================
# ROTAS: QUESTÕES & ALTERNATIVAS
# =========================================================

@app.post("/questoes")
def cadastrar_questao(questao: QuestaoCadastro):
    try:
        # 1. Insere os dados da questão principal na tabela 'questoes'
        res_questao = supabase.table("questoes").insert({
            "professor_id": str(questao.professor_id),
            "disciplina_id": str(questao.disciplina_id),
            "tema_id": str(questao.tema_id) if questao.tema_id else None,
            "tipo": "multipla_escolha",
            "nivel": questao.nivel,
            "enunciado": questao.enunciado,
            "explicacao": questao.explicacao,
            "pontos": questao.pontos
        }).execute()
        
        questao_id = res_questao.data[0]["id"]

        # 2. Prepara e insere a lista de alternativas vinculadas na tabela 'alternativas'
        alternativas_db = []
        for index, texto in enumerate(questao.alternativas):
            alternativas_db.append({
                "questao_id": questao_id,
                "texto": texto,
                "correta": (index == questao.index_correta),
                "ordem": index + 1
            })
            
        supabase.table("alternativas").insert(alternativas_db).execute()

        return {
            "mensagem": "Questão e alternativas cadastradas com sucesso",
            "id": questao_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/questoes")
def listar_questoes():
    # Retorna todas as questões realizando um JOIN automático para trazer as alternativas juntas
    result = supabase.table("questoes").select("*, alternativas(*)").execute()
    return result.data

# =========================================================
# ROTAS: MINI-PROVAS (Geração Dinâmica e Registro de Tentativa)
# =========================================================

@app.get("/mini-prova/{prova_id}/aluno/{aluno_id}")
def iniciar_mini_prova(prova_id: UUID, aluno_id: UUID):
    try:
        # 1. Busca os dados da mini-prova no banco e valida o status
        res_prova = supabase.table("mini_provas").select("*").eq("id", str(prova_id)).single().execute()
        prova = res_prova.data
        
        if not prova:
            raise HTTPException(status_code=404, detail="Mini-prova não encontrada.")
        if prova["status"] != "liberada":
            raise HTTPException(status_code=400, detail=f"Esta prova não está disponível. Status atual: {prova['status']}")

        # 2. Busca os IDs das questões vinculadas a essa prova (tabela prova_questoes)
        res_pq = supabase.table("prova_questoes").select("questao_id").eq("prova_id", str(prova_id)).execute()
        questoes_ids = [item["questao_id"] for item in res_pq.data]

        if not questoes_ids:
            raise HTTPException(status_code=400, detail="Esta prova ainda não possui questões vinculadas.")

        # 3. Busca o conteúdo completo das questões encontradas e de suas alternativas
        res_questoes = supabase.table("questoes").select("*, alternativas(*)").in_("id", questoes_ids).execute()
        questoes_completas = res_questoes.data

        # 4. Cria de forma oficial o registro da 'tentativa' no banco de dados
        # Descobre o número da tentativa do aluno para esta prova específica
        res_tentativas_anteriores = supabase.table("tentativas").select("numero").eq("prova_id", str(prova_id)).eq("aluno_id", str(aluno_id)).execute()
        proximo_numero = len(res_tentativas_anteriores.data) + 1

        res_tentativa = supabase.table("tentativas").insert({
            "prova_id": str(prova_id),
            "aluno_id": str(aluno_id),
            "numero": proximo_numero,
            "tempo_concedido_min": prova["duracao_minutos"],
            "status": "em_andamento"
        }).execute()
        
        tentativa_id = res_tentativa.data[0]["id"]

        # 5. Organiza o payload de retorno respeitando as regras de randomização
        payload_questoes = []
        for q in questoes_completas:
            alts = [{"id": a["id"], "texto": a["texto"]} for a in q["alternativas"]]
            if prova["randomizar_alternativas"]:
                random.shuffle(alts)
                
            payload_questoes.append({
                "id": q["id"],
                "enunciado": q["enunciado"],
                "nivel": q["nivel"],
                "pontos": q["pontos"],
                "alternativas": alts
            })

        if prova["randomizar_questoes"]:
            random.shuffle(payload_questoes)

        return {
            "tentativa_id": tentativa_id,
            "prova_titulo": prova["titulo"],
            "duracao_minutos": prova["duracao_minutos"],
            "quantidade_questoes": len(payload_questoes),
            "questoes": payload_questoes
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# =========================================================
# ROTAS: CORREÇÃO INTELIGENTE
# =========================================================

@app.post("/corrigir")
def corrigir_prova(correcao: Correcao):
    try:
        # 1. Localiza a tentativa informada e valida se ela continua em andamento
        res_tentativa = supabase.table("tentativas").select("*").eq("id", str(correcao.tentativa_id)).single().execute()
        tentativa = res_tentativa.data

        if not tentativa:
            raise HTTPException(status_code=404, detail="Tentativa não localizada.")
        if tentativa["status"] != "em_andamento":
            raise HTTPException(status_code=400, detail=f"Esta tentativa não pode ser corrigida pois está com status: {tentativa['status']}")

        nota_final = 0.0
        respostas_db = []

        # 2. Varre as respostas enviadas pelo aluno para calcular os acertos e notas
        for resp in correcao.respostas:
            # Puxa qual é a alternativa correta oficial registrada para a questão
            res_alt = supabase.table("alternativas").select("*").eq("questao_id", str(resp.questao_id)).eq("correta", True).single().execute()
            alt_correta = res_alt.data

            # Puxa o valor em pontos atribuído àquela questão específica
            res_q = supabase.table("questoes").select("pontos").eq("id", str(resp.questao_id)).single().execute()
            pontos_questao = float(res_q.data["pontos"])

            # Compara a resposta enviada com o ID correto do banco
            eh_correta = (str(resp.alternativa_id) == alt_correta["id"])
            pontos_ganhos = pontos_questao if eh_correta else 0.0
            nota_final += pontos_ganhos

            # Estrutura a inserção para a tabela 'respostas'
            respostas_db.append({
                "tentativa_id": str(correcao.tentativa_id),
                "questao_id": str(resp.questao_id),
                "alternativa_id": str(resp.alternativa_id),
                "correta": eh_correta,
                "nota": pontos_ganhos,
                "respondida_em": "now()"
            })

        # 3. Salva em lote (bulk insert) todas as respostas enviadas na tabela 'respostas'
        if respostas_db:
            supabase.table("respostas").insert(respostas_db).execute()

        # 4. Atualiza o status da Tentativa para 'finalizada' e armazena a pontuação obtida
        supabase.table("tentativas").update({
            "status": "finalizada",
            "status_correcao": "automatica",
            "nota_final": nota_final,
            "finished_at": "now()"
        }).eq("id", str(correcao.tentativa_id)).execute()

        return {
            "mensagem": "Prova processada e corrigida com sucesso.",
            "tentativa_id": correcao.tentativa_id,
            "nota_final": round(nota_final, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# =========================================================
# ROTAS: FILTROS ATUALIZADOS POR ID (UUID)
# =========================================================

@app.get("/questoes/disciplina/{disciplina_id}")
def filtrar_disciplina(disciplina_id: UUID):
    result = supabase.table("questoes").select("*").eq("disciplina_id", str(disciplina_id)).execute()
    return result.data

@app.get("/questoes/dificuldade/{dificuldade}")
def filtrar_dificuldade(dificuldade: str):
    # Aceita os valores mapeados no ENUM nivel_dificuldade: 'facil', 'intermediario', 'dificil'
    result = supabase.table("questoes").select("*").eq("nivel", dificuldade).execute()
    return result.data

# =========================================================
# ROTAS: HISTÓRICO E LOGS
# =========================================================

@app.get("/relatorios/diarios")
def listar_resultados_diarios():
    # Retorna o histórico de desempenho estruturado da nova tabela de consolidação diária
    result = supabase.table("resultados_diarios").select("*").execute()
    return result.data

@app.get("/logs")
def ver_logs_sistema():
    # Retorna a tabela real de auditoria de eventos mapeada no script SQL
    result = supabase.table("logs_execucao").select("*").order("created_at", desc=True).execute()
    return result.data
