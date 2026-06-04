import os
from supabase import create_client, Client
from typing import List, Dict, Any, Optional

# ==========================================
# 1. CONFIG & DATABASE SETUP
# ==========================================
SUPABASE_URL = os.environ.get("SUPABASE_URL", "YOUR-SUPABASE-URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "YOUR-SUPABASE-KEY")

banco: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ==========================================
# 2. REPOSITORY LAYER (Agnóstica de Regras)
# O único objetivo desta camada é executar queries SQL via supabase-py.
# Nenhuma regra de negócio (validações, lógicas de acerto) existe aqui.
# ==========================================
def repo_get_usuario(usuario_id: int) -> Optional[Dict[str, Any]]:
    res = banco.table("usuarios").select("*").eq("id", usuario_id).single().execute()
    return res.data if res.data else None


def repo_insert_quiz(dados_quiz: Dict[str, Any]) -> Dict[str, Any]:
    res = banco.table("quizzes").insert(dados_quiz).execute()
    return res.data[0]


def repo_get_quiz(quiz_id: int) -> Optional[Dict[str, Any]]:
    res = banco.table("quizzes").select("*").eq("id", quiz_id).single().execute()
    return res.data if res.data else None


def repo_update_quiz_status(quiz_id: int, status: str) -> Dict[str, Any]:
    res = banco.table("quizzes").update({"status": status}).eq("id", quiz_id).execute()
    return res.data[0]


def repo_insert_pergunta(dados_perguntas_quizaovivo: Dict[str, Any]) -> Dict[str, Any]:
    res = banco.table("perguntas_quizaovivo").insert(dados_perguntas_quizaovivo).execute()
    return res.data[0]


def repo_get_pergunta(pergunta_id: int) -> Optional[Dict[str, Any]]:
    res = banco.table("perguntas_quizaovivo").select("*").eq("id", pergunta_id).single().execute()
    return res.data if res.data else None


def repo_get_perguntas_quizaovivo(quiz_id: int) -> List[Dict[str, Any]]:
    res = banco.table("perguntas_quizaovivo").select("*").eq("quiz_id", quiz_id).order("id").execute()
    return res.data


def repo_insert_participacao_quizaovivo(dados_participacao_quizaovivo: Dict[str, Any]) -> Dict[str, Any]:
    res = banco.table("participacao_quizaovivo").insert(dados_participacao_quizaovivo).execute()
    return res.data[0]


def repo_get_participacao_quizaovivo(participacao_quizaovivo_id: int) -> Optional[Dict[str, Any]]:
    res = banco.table("participacao_quizaovivo").select("*").eq("id", participacao_quizaovivo_id).single().execute()
    return res.data if res.data else None


def repo_get_participacao_por_aluno_quiz(aluno_id: int, quiz_id: int) -> Optional[Dict[str, Any]]:
    res = banco.table("participacao_quizaovivo").select("*").eq("aluno_id", aluno_id).eq("quiz_id", quiz_id).single().execute()
    return res.data if res.data else None


def repo_update_pontuacao_participacao(participacao_id: int, nova_pontuacao: int) -> Dict[str, Any]:
    res = banco.table("participacao_quizaovivo").update({"pontuacao": nova_pontuacao}).eq("id", participacao_id).execute()
    return res.data[0]


def repo_insert_resposta_quizaovivo(dados_resposta_quizaovivo: Dict[str, Any]) -> Dict[str, Any]:
    res = banco.table("respostas_quizaovivo").insert(dados_resposta_quizaovivo).execute()
    return res.data[0]


def repo_get_ranking_quiz(quiz_id: int):
    res = banco.table("participacao_quizaovivo") \
        .select("*") \
        .eq("quiz_id", quiz_id) \
        .order("pontuacao", desc=True) \
        .execute()

    return res.data


# ==========================================
# 3. SERVICE LAYER (Regras de Negócio e Segurança)
# Esta camada orquestra a lógica, validações (Guarda-Costas)
# e utiliza a Repository Layer para interagir com o DB.
# ==========================================
def _verificar_permissao_professor(usuario_id: int) -> tuple[bool, str]:
    """O Guarda-Costas interno dos services. Retorna (Permitido?, Motivo)"""
    try:
        usuario = repo_get_usuario(usuario_id)
        if not usuario:
            return False, f"Usuário (ID: {usuario_id}) não encontrado no banco de dados."

        tipo = str(usuario.get("tipo_usuario")).strip().lower()
        if tipo != "professor":
            return False, f"O tipo de usuário é '{usuario.get('tipo_usuario')}', mas exige-se 'professor'."

        return True, "Permitido"
    except Exception as e:
        return False, f"Erro de conexão com o Supabase ao verificar usuário: {str(e)}"


# --- SERVIÇOS DO PROFESSOR ---
def criar_quiz(titulo: str, professor_id: int) -> Dict[str, Any]:
    titulo = titulo.strip() if titulo else ""
    if len(titulo) < 3:
        return {"sucesso": False, "mensagem": "O título deve ter pelo menos 3 caracteres."}

    permitido, motivo = _verificar_permissao_professor(professor_id)
    if not permitido:
        return {"sucesso": False, "mensagem": f"Acesso negado: {motivo}"}
    novo_quiz = {
        "titulo": titulo,
        "professor_id": professor_id,
        "status": "pendente"
    }

    try:
        dados = repo_insert_quiz(novo_quiz)
        return {"sucesso": True, "dados": dados}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro interno no banco de dados: {str(e)}"}


def adicionar_pergunta(quiz_id: int, professor_id: int, texto: str, alternativas: List[str], indice_correto: int) -> \
Dict[str, Any]:
    permitido, motivo = _verificar_permissao_professor(professor_id)
    if not permitido:
        return {"sucesso": False, "mensagem": f"Acesso negado: {motivo}"}
    if len(alternativas) < 2:
        return {"sucesso": False, "mensagem": "A pergunta deve ter pelo menos 2 alternativas."}

    if indice_correto < 0 or indice_correto >= len(alternativas):
        return {"sucesso": False, "mensagem": "Índice da alternativa correta é inválido."}
    try:
        def repo_get_quiz(quiz_id: int):
            res = banco.table("quizzes") \
                .select("*") \
                .eq("id", quiz_id) \
                .single() \
                .execute()

            return res.data if res.data else None
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro ao verificar quiz: {str(e)}"}
    nova_pergunta = {
        "quiz_id": quiz_id,
        "texto": texto,
        "alternativas": alternativas,
        "indice_correto": indice_correto
    }
    try:
        dados = repo_insert_pergunta(nova_pergunta)
        return {"sucesso": True, "dados": dados}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro ao adicionar pergunta: {str(e)}"}


def alterar_status_quiz(quiz_id: int, professor_id: int, novo_status: str) -> Dict[str, Any]:
    permitido, motivo = _verificar_permissao_professor(professor_id)
    if not permitido:
        return {"sucesso": False, "mensagem": f"Acesso negado: {motivo}"}
    if novo_status not in ["iniciado", "finalizado"]:
        return {"sucesso": False, "mensagem": "Status inválido."}
    try:
        quiz = repo_get_quiz(quiz_id)
        if not quiz or quiz["professor_id"] != professor_id:
            return {"sucesso": False, "mensagem": "Quiz não encontrado ou não pertence a você."}

        if quiz["status"] == "finalizado":
            return {"sucesso": False, "mensagem": "O quiz já foi finalizado."}
        dados = repo_update_quiz_status(quiz_id, novo_status)
        return {"sucesso": True, "dados": dados}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro ao alterar status: {str(e)}"}


# --- SERVIÇOS DO ALUNO ---
def entrar_quiz(aluno_id: int, quiz_id: int) -> Dict[str, Any]:
    try:
        quiz = repo_get_quiz(quiz_id)
        if not quiz or quiz["status"] != "iniciado":
            return {"sucesso": False, "mensagem": "Quiz indisponível ou já finalizado."}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro ao buscar quiz: {str(e)}"}
    nova_participacao = {
        "quiz_id": quiz_id,
        "aluno_id": aluno_id,
        "pontuacao": 0,
        "finalizou": False
    }
    try:
        dados = repo_insert_participacao_quizaovivo(nova_participacao)
        return {"sucesso": True, "dados": dados}
    except Exception as e:
        if "unique constraint" in str(e).lower():
            try:
                existente = repo_get_participacao_por_aluno_quiz(aluno_id, quiz_id)
                return {"sucesso": True, "mensagem": "Aluno já ingressado neste quiz.", "dados": existente}
            except Exception as e_interno:
                return {"sucesso": False, "mensagem": f"Erro ao recuperar participação existente: {str(e_interno)}"}
        return {"sucesso": False, "mensagem": f"Erro ao ingressar no quiz: {str(e)}"}


def responder_pergunta(participacao_id: int, pergunta_id: int, indice_resposta: int) -> Dict[str, Any]:
    try:
        participacao = repo_get_participacao_quizaovivo(participacao_id)
        if not participacao or participacao["finalizou"]:
            return {"sucesso": False, "mensagem": "Participação inválida ou quiz já finalizado."}

        pergunta = repo_get_pergunta(pergunta_id)
        if not pergunta:
            return {"sucesso": False, "mensagem": "Pergunta não encontrada."}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro ao validar dados: {str(e)}"}
    correta = (indice_resposta == pergunta["indice_correto"])

    nova_resposta = {
        "participacao_id": participacao_id,
        "pergunta_id": pergunta_id,
        "indice_resposta": indice_resposta,
        "correta": correta
    }
    try:
        dados_resposta = repo_insert_resposta_quizaovivo(nova_resposta)

        if correta:
            # Gamificação: Adiciona 10 pontos
            nova_pontuacao = participacao["pontuacao"] + 10
            repo_update_pontuacao_participacao(participacao_id, nova_pontuacao)
        return {
            "sucesso": True,
            "dados": {
                "resposta_registrada": dados_resposta,
                "correta": correta,
                "feedback": "Resposta correta!" if correta else "Resposta incorreta."
            }
        }
    except Exception as e:
        if "unique constraint" in str(e).lower():
            return {"sucesso": False, "mensagem": "Você já respondeu esta pergunta."}
        return {"sucesso": False, "mensagem": f"Erro ao registrar resposta: {str(e)}"}


def obter_ranking(quiz_id: int) -> Dict[str, Any]:
    try:
        ranking = repo_get_ranking_quiz(quiz_id)
        return {"sucesso": True, "dados": ranking}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro ao obter ranking: {str(e)}"}


def obter_perguntas_quizaovivo(quiz_id: int) -> Dict[str, Any]:
    try:
        perguntas_quizaovivo = repo_get_perguntas_quizaovivo(quiz_id)
        # Ocultar o índice correto por segurança
        for p in perguntas_quizaovivo:
            p.pop("indice_correto", None)
        return {"sucesso": True, "dados": perguntas_quizaovivo}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro ao obter perguntas: {str(e)}"}

