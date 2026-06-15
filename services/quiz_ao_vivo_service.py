import os
from typing import Any, Dict, List, Optional, Tuple

from supabase import Client, create_client


SUPABASE_URL = os.environ.get("SUPABASE_URL", "YOUR-SUPABASE-URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "YOUR-SUPABASE-KEY")

banco: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ==========================================
# Repository layer
# ==========================================
def _first_row(data: Any) -> Optional[Dict[str, Any]]:
    if isinstance(data, list):
        return data[0] if data else None
    return data if data else None


def repo_get_usuario(usuario_id: int) -> Optional[Dict[str, Any]]:
    res = (
        banco.table("usuarios")
        .select("*")
        .eq("id", usuario_id)
        .limit(1)
        .execute()
    )
    return _first_row(res.data)


def repo_insert_quiz(dados_quiz: Dict[str, Any]) -> Dict[str, Any]:
    res = banco.table("quizzes").insert(dados_quiz).execute()
    return _first_row(res.data) or {}


def repo_get_quiz(quiz_id: int) -> Optional[Dict[str, Any]]:
    res = (
        banco.table("quizzes")
        .select("*")
        .eq("id", quiz_id)
        .limit(1)
        .execute()
    )
    return _first_row(res.data)


def repo_update_quiz_status(quiz_id: int, status: str) -> Optional[Dict[str, Any]]:
    res = (
        banco.table("quizzes")
        .update({"status": status})
        .eq("id", quiz_id)
        .execute()
    )
    return _first_row(res.data)


def repo_update_pergunta_atual(
    quiz_id: int,
    pergunta_atual: int,
) -> Optional[Dict[str, Any]]:
    res = (
        banco.table("quizzes")
        .update({"pergunta_atual": pergunta_atual})
        .eq("id", quiz_id)
        .execute()
    )
    return _first_row(res.data)


def repo_update_quiz_inicio(quiz_id: int) -> Optional[Dict[str, Any]]:
    res = (
        banco.table("quizzes")
        .update({"status": "iniciado", "pergunta_atual": 0})
        .eq("id", quiz_id)
        .execute()
    )
    return _first_row(res.data)


def repo_insert_pergunta(dados_pergunta: Dict[str, Any]) -> Dict[str, Any]:
    res = banco.table("perguntas_quizaovivo").insert(dados_pergunta).execute()
    return _first_row(res.data) or {}


def repo_get_pergunta(pergunta_id: int) -> Optional[Dict[str, Any]]:
    res = (
        banco.table("perguntas_quizaovivo")
        .select("*")
        .eq("id", pergunta_id)
        .limit(1)
        .execute()
    )
    return _first_row(res.data)


def repo_get_perguntas_quizaovivo(quiz_id: int) -> List[Dict[str, Any]]:
    res = (
        banco.table("perguntas_quizaovivo")
        .select("*")
        .eq("quiz_id", quiz_id)
        .order("id")
        .execute()
    )
    return res.data or []


def repo_insert_participacao_quizaovivo(
    dados_participacao: Dict[str, Any],
) -> Dict[str, Any]:
    res = banco.table("participacao_quizaovivo").insert(dados_participacao).execute()
    return _first_row(res.data) or {}


def repo_get_participacao_quizaovivo(
    participacao_id: int,
) -> Optional[Dict[str, Any]]:
    res = (
        banco.table("participacao_quizaovivo")
        .select("*")
        .eq("id", participacao_id)
        .limit(1)
        .execute()
    )
    return _first_row(res.data)


def repo_get_participacao_por_aluno_quiz(
    aluno_id: int,
    quiz_id: int,
) -> Optional[Dict[str, Any]]:
    res = (
        banco.table("participacao_quizaovivo")
        .select("*")
        .eq("aluno_id", aluno_id)
        .eq("quiz_id", quiz_id)
        .limit(1)
        .execute()
    )
    return _first_row(res.data)


def repo_update_pontuacao_participacao(
    participacao_id: int,
    nova_pontuacao: int,
) -> Optional[Dict[str, Any]]:
    res = (
        banco.table("participacao_quizaovivo")
        .update({"pontuacao": nova_pontuacao})
        .eq("id", participacao_id)
        .execute()
    )
    return _first_row(res.data)


def repo_insert_resposta_quizaovivo(
    dados_resposta: Dict[str, Any],
) -> Dict[str, Any]:
    res = banco.table("respostas_quizaovivo").insert(dados_resposta).execute()
    return _first_row(res.data) or {}


def repo_get_resposta_por_participacao_pergunta(
    participacao_id: int,
    pergunta_id: int,
) -> Optional[Dict[str, Any]]:
    res = (
        banco.table("respostas_quizaovivo")
        .select("*")
        .eq("participacao_id", participacao_id)
        .eq("pergunta_id", pergunta_id)
        .limit(1)
        .execute()
    )
    return _first_row(res.data)


def repo_get_ranking_quiz(quiz_id: int) -> List[Dict[str, Any]]:
    res = (
        banco.table("participacao_quizaovivo")
        .select("pontuacao, usuarios(nome)")
        .eq("quiz_id", quiz_id)
        .order("pontuacao", desc=True)
        .execute()
    )
    return res.data or []


# ==========================================
# Service layer
# ==========================================
def _ok(dados: Any = None, mensagem: Optional[str] = None) -> Dict[str, Any]:
    resposta = {"sucesso": True}
    if dados is not None:
        resposta["dados"] = dados
    if mensagem:
        resposta["mensagem"] = mensagem
    return resposta


def _erro(mensagem: str) -> Dict[str, Any]:
    return {"sucesso": False, "mensagem": mensagem}


def _verificar_permissao_professor(usuario_id: int) -> Tuple[bool, str]:
    try:
        usuario = repo_get_usuario(usuario_id)
        if not usuario:
            return False, f"Usuario (ID: {usuario_id}) nao encontrado."

        tipo = str(usuario.get("tipo_usuario", "")).strip().lower()
        if tipo != "professor":
            return False, f"O tipo de usuario e '{usuario.get('tipo_usuario')}', mas exige-se 'professor'."

        return True, "Permitido"
    except Exception as exc:
        return False, f"Erro ao verificar usuario no Supabase: {exc}"


def _validar_professor_dono_quiz(
    quiz_id: int,
    professor_id: int,
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
    permitido, motivo = _verificar_permissao_professor(professor_id)
    if not permitido:
        return None, _erro(f"Acesso negado: {motivo}")

    quiz = repo_get_quiz(quiz_id)
    if not quiz:
        return None, _erro("Quiz nao encontrado.")

    if quiz.get("professor_id") != professor_id:
        return None, _erro("Este quiz pertence a outro professor.")

    return quiz, None


# --- Professor ---
def criar_quiz(titulo: str, professor_id: int) -> Dict[str, Any]:
    titulo = titulo.strip() if titulo else ""
    if len(titulo) < 3:
        return _erro("O titulo deve ter pelo menos 3 caracteres.")

    permitido, motivo = _verificar_permissao_professor(professor_id)
    if not permitido:
        return _erro(f"Acesso negado: {motivo}")

    novo_quiz = {
        "titulo": titulo,
        "professor_id": professor_id,
        "status": "pendente",
        "pergunta_atual": None,
    }

    try:
        return _ok(repo_insert_quiz(novo_quiz))
    except Exception as exc:
        return _erro(f"Erro interno no banco de dados: {exc}")


def adicionar_pergunta(
    quiz_id: int,
    professor_id: int,
    texto: str,
    alternativas: List[str],
    indice_correto: int,
) -> Dict[str, Any]:
    texto = texto.strip() if texto else ""
    alternativas_limpas = [alt.strip() for alt in alternativas if alt and alt.strip()]

    if len(texto) < 3:
        return _erro("O texto da pergunta deve ter pelo menos 3 caracteres.")

    if len(alternativas_limpas) < 2:
        return _erro("A pergunta deve ter pelo menos 2 alternativas.")

    if indice_correto < 0 or indice_correto >= len(alternativas_limpas):
        return _erro("Indice da alternativa correta e invalido.")

    try:
        _, erro = _validar_professor_dono_quiz(quiz_id, professor_id)
        if erro:
            return erro

        nova_pergunta = {
            "quiz_id": quiz_id,
            "texto": texto,
            "alternativas": alternativas_limpas,
            "indice_correto": indice_correto,
        }
        return _ok(repo_insert_pergunta(nova_pergunta))
    except Exception as exc:
        return _erro(f"Erro ao adicionar pergunta: {exc}")


def alterar_status_quiz(
    quiz_id: int,
    professor_id: int,
    novo_status: str,
) -> Dict[str, Any]:
    if novo_status not in {"iniciado", "finalizado"}:
        return _erro("Status invalido.")

    try:
        quiz, erro = _validar_professor_dono_quiz(quiz_id, professor_id)
        if erro:
            return erro

        if quiz and quiz.get("status") == "finalizado":
            return _erro("O quiz ja foi finalizado.")

        if novo_status == "iniciado":
            perguntas = repo_get_perguntas_quizaovivo(quiz_id)
            if not perguntas:
                return _erro("Nao e possivel iniciar um quiz sem perguntas.")
            dados = repo_update_quiz_inicio(quiz_id)
        else:
            dados = repo_update_quiz_status(quiz_id, novo_status)

        if not dados:
            return _erro("O status do quiz nao foi atualizado no Supabase.")

        return _ok(dados)
    except Exception as exc:
        return _erro(f"Erro ao alterar status: {exc}")


def avancar_pergunta(quiz_id: int, professor_id: int) -> Dict[str, Any]:
    try:
        quiz, erro = _validar_professor_dono_quiz(quiz_id, professor_id)
        if erro:
            return erro

        if quiz and quiz.get("status") != "iniciado":
            return _erro("Somente quizzes iniciados podem avancar pergunta.")

        perguntas = repo_get_perguntas_quizaovivo(quiz_id)
        if not perguntas:
            return _erro("Este quiz nao possui perguntas.")

        atual = quiz.get("pergunta_atual") if quiz else None
        if atual is None:
            atual = 0
        else:
            atual = int(atual)

        proxima = atual + 1
        if proxima >= len(perguntas):
            return _erro("Nao ha proxima pergunta.")

        dados = repo_update_pergunta_atual(quiz_id, proxima)
        if not dados:
            return _erro("A pergunta atual nao foi atualizada no Supabase.")

        return _ok(dados)
    except Exception as exc:
        return _erro(f"Erro ao avancar pergunta: {exc}")


# --- Aluno ---
def entrar_quiz(aluno_id: int, quiz_id: int) -> Dict[str, Any]:
    try:
        quiz = repo_get_quiz(quiz_id)
        if not quiz or quiz.get("status") != "iniciado":
            return _erro("Quiz indisponivel ou ja finalizado.")

        existente = repo_get_participacao_por_aluno_quiz(aluno_id, quiz_id)
        if existente:
            return _ok(existente, "Aluno ja ingressado neste quiz.")

        nova_participacao = {
            "quiz_id": quiz_id,
            "aluno_id": aluno_id,
            "pontuacao": 0,
            "finalizou": False,
        }
        return _ok(repo_insert_participacao_quizaovivo(nova_participacao))
    except Exception as exc:
        mensagem = str(exc)
        if "unique" in mensagem.lower():
            existente = repo_get_participacao_por_aluno_quiz(aluno_id, quiz_id)
            if existente:
                return _ok(existente, "Aluno ja ingressado neste quiz.")
        return _erro(f"Erro ao ingressar no quiz: {mensagem}")


def obter_participacao(participacao_id: int) -> Dict[str, Any]:
    try:
        participacao = repo_get_participacao_quizaovivo(participacao_id)
        if not participacao:
            return _erro("Participacao nao encontrada.")
        return _ok(participacao)
    except Exception as exc:
        return _erro(f"Erro ao obter participacao: {exc}")


def obter_pergunta_atual_quiz(quiz_id: int) -> Dict[str, Any]:
    try:
        quiz = repo_get_quiz(quiz_id)
        if not quiz:
            return _erro("Quiz nao encontrado.")

        perguntas = repo_get_perguntas_quizaovivo(quiz_id)
        atual = quiz.get("pergunta_atual")

        if quiz.get("status") != "iniciado":
            return _ok({"quiz": quiz, "pergunta": None, "indice": atual})

        if atual is None:
            return _erro("Quiz iniciado sem pergunta_atual definida.")

        indice = int(atual)
        if indice < 0 or indice >= len(perguntas):
            return _ok({"quiz": quiz, "pergunta": None, "indice": indice, "fim": True})

        pergunta = dict(perguntas[indice])
        pergunta.pop("indice_correto", None)

        return _ok(
            {
                "quiz": quiz,
                "pergunta": pergunta,
                "indice": indice,
                "total": len(perguntas),
                "fim": False,
            }
        )
    except Exception as exc:
        return _erro(f"Erro ao obter pergunta atual: {exc}")


def responder_pergunta(
    participacao_id: int,
    pergunta_id: int,
    indice_resposta: int,
) -> Dict[str, Any]:
    try:
        participacao = repo_get_participacao_quizaovivo(participacao_id)
        if not participacao or participacao.get("finalizou"):
            return _erro("Participacao invalida ou quiz ja finalizado.")

        pergunta = repo_get_pergunta(pergunta_id)
        if not pergunta:
            return _erro("Pergunta nao encontrada.")

        quiz = repo_get_quiz(participacao["quiz_id"])
        if not quiz or quiz.get("status") != "iniciado":
            return _erro("Quiz indisponivel para respostas.")

        perguntas = repo_get_perguntas_quizaovivo(participacao["quiz_id"])
        atual = quiz.get("pergunta_atual")
        if atual is None:
            return _erro("Quiz iniciado sem pergunta_atual definida.")

        indice_atual = int(atual)
        if indice_atual < 0 or indice_atual >= len(perguntas):
            return _erro("Nao ha pergunta atual para responder.")

        pergunta_atual = perguntas[indice_atual]
        if pergunta_atual.get("id") != pergunta_id:
            return _erro("Esta pergunta nao e a pergunta atual do quiz.")

        resposta_existente = repo_get_resposta_por_participacao_pergunta(
            participacao_id,
            pergunta_id,
        )
        if resposta_existente:
            return _erro("Voce ja respondeu esta pergunta.")

        alternativas = pergunta.get("alternativas") or []
        if indice_resposta < 0 or indice_resposta >= len(alternativas):
            return _erro("Indice da resposta e invalido.")

        correta = indice_resposta == pergunta.get("indice_correto")
        nova_resposta = {
            "participacao_id": participacao_id,
            "pergunta_id": pergunta_id,
            "indice_resposta": indice_resposta,
            "correta": correta,
        }

        dados_resposta = repo_insert_resposta_quizaovivo(nova_resposta)
        pontuacao_atual = int(participacao.get("pontuacao") or 0)
        nova_pontuacao = pontuacao_atual + 10 if correta else pontuacao_atual

        if correta:
            repo_update_pontuacao_participacao(participacao_id, nova_pontuacao)

        return _ok(
            {
                "resposta_registrada": dados_resposta,
                "correta": correta,
                "feedback": "Resposta correta!" if correta else "Resposta incorreta.",
                "pontuacao": nova_pontuacao,
            }
        )
    except Exception as exc:
        if "unique" in str(exc).lower():
            return _erro("Voce ja respondeu esta pergunta.")
        return _erro(f"Erro ao registrar resposta: {exc}")


def obter_ranking(quiz_id: int) -> Dict[str, Any]:
    try:
        return _ok(repo_get_ranking_quiz(quiz_id))
    except Exception as exc:
        return _erro(f"Erro ao obter ranking: {exc}")


def obter_perguntas_quizaovivo(quiz_id: int) -> Dict[str, Any]:
    try:
        perguntas = repo_get_perguntas_quizaovivo(quiz_id)
        perguntas_sem_gabarito = []
        for pergunta in perguntas:
            segura = dict(pergunta)
            segura.pop("indice_correto", None)
            perguntas_sem_gabarito.append(segura)
        return _ok(perguntas_sem_gabarito)
    except Exception as exc:
        return _erro(f"Erro ao obter perguntas: {exc}")

