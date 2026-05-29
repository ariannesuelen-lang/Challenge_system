
import logging
from database.conexao import supabase

logger = logging.getLogger(__name__)


def _execute(query):
    try:
        result = query.execute()
    except Exception as exc:
        logger.exception("Erro ao executar query Supabase: %s", exc)
        return None
    if result is None:
        return None
    if hasattr(result, "error") and result.error:
        logger.error("Erro do Supabase: %s", result.error)
        return None
    return result


# --------------------------------------------------
# TIMES
# --------------------------------------------------

def listar_times():
    res = _execute(supabase.table("times").select("*").order("id"))
    return res.data if res else []


def criar_time(nome):
    if not nome or not nome.strip():
        return False
    res = _execute(supabase.table("times").insert({"nome": nome.strip()}))
    return res is not None


def editar_time(time_id, nome):
    if not nome or not nome.strip():
        return False
    res = _execute(
        supabase.table("times").update({"nome": nome.strip()}).eq("id", int(time_id))
    )
    return res is not None


def deletar_time(time_id):
    res = _execute(supabase.table("times").delete().eq("id", int(time_id)))
    return res is not None


# --------------------------------------------------
# MEMBROS
# --------------------------------------------------

def listar_membros_time(time_id):
    try:
        time_id = int(time_id)
    except (TypeError, ValueError):
        return []
    res = _execute(
        supabase.table("time_membros")
        .select("usuario_id, usuarios(id,nome,email)")
        .eq("time_id", time_id)
    )
    if not res:
        return []
    membros = []
    for r in (res.data or []):
        if not isinstance(r, dict):
            continue
        u = r.get("usuarios")
        if not isinstance(u, dict):
            continue
        if u.get("id") and u.get("nome"):
            membros.append({
                "id":    u["id"],
                "nome":  u["nome"],
                "email": u.get("email", "")
            })
    return membros


def listar_alunos():
    res = _execute(
        supabase.table("usuarios").select("id,nome").eq("tipo_usuario", "aluno")
    )
    return res.data if res else []


def obter_time_do_aluno(user_id):
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return None
    res = _execute(
        supabase.table("time_membros")
        .select("time_id")
        .eq("usuario_id", user_id)
        .limit(1)
    )
    if not res or not res.data:
        return None
    row = res.data[0]
    if not isinstance(row, dict):
        return None
    try:
        return int(row.get("time_id"))
    except (TypeError, ValueError):
        return None


def aluno_tem_time(user_id):
    return obter_time_do_aluno(user_id) is not None


def definir_time_usuario(user_id, time_id):
    try:
        user_id = int(user_id)
        time_id = int(time_id)
    except (TypeError, ValueError):
        return False
    _execute(supabase.table("time_membros").delete().eq("usuario_id", user_id))
    res = _execute(
        supabase.table("time_membros").insert({"time_id": time_id, "usuario_id": user_id})
    )
    return res is not None


def entrar_no_time(time_id, user_id):
    if aluno_tem_time(user_id):
        return False
    return definir_time_usuario(user_id, time_id)


def adicionar_aluno(time_id, user_id):
    if aluno_tem_time(user_id):
        return False
    return definir_time_usuario(user_id, time_id)


def remover_aluno(time_id, user_id):
    try:
        time_id = int(time_id)
        user_id = int(user_id)
    except (TypeError, ValueError):
        return False
    res = _execute(
        supabase.table("time_membros")
        .delete()
        .eq("time_id", time_id)
        .eq("usuario_id", user_id)
    )
    return res is not None


def mover_aluno(user_id, time_destino):
    return definir_time_usuario(user_id, time_destino)


# --------------------------------------------------
# BATALHAS
# --------------------------------------------------

def listar_batalhas():
    res = _execute(supabase.table("batalhas").select("*").order("id"))
    return res.data if res else []


def criar_batalha(titulo, descricao, criador_id, prazo=None):
    payload = {
        "titulo":     titulo.strip(),
        "descricao":  descricao.strip() if descricao else "",
        "criador_id": int(criador_id),
        "finalizada": False,
    }
    if prazo:
        payload["prazo"] = str(prazo)
    res = _execute(supabase.table("batalhas").insert(payload))
    return res is not None


def finalizar_batalha(batalha_id):
    res = _execute(
        supabase.table("batalhas")
        .update({"finalizada": True})
        .eq("id", int(batalha_id))
    )
    return res is not None


def obter_batalha(batalha_id):
    res = _execute(
        supabase.table("batalhas").select("*").eq("id", int(batalha_id)).limit(1)
    )
    if not res or not res.data:
        return None
    return res.data[0]


# --------------------------------------------------
# RESPOSTAS DE BATALHA
# --------------------------------------------------

def enviar_resposta_batalha(batalha_id, user_id, conteudo):
    if not conteudo or not conteudo.strip():
        return False
    res = _execute(supabase.table("respostas_batalha").insert({
        "batalha_id": int(batalha_id),
        "usuario_id": int(user_id),
        "conteudo":   conteudo.strip(),
    }))
    return res is not None


def listar_respostas_batalha(batalha_id):
    res = _execute(
        supabase.table("respostas_batalha")
        .select("*, usuarios(nome)")
        .eq("batalha_id", int(batalha_id))
        .order("criado_em")
    )
    return res.data if res else []


def usuario_ja_respondeu(batalha_id, user_id):
    res = _execute(
        supabase.table("respostas_batalha")
        .select("id")
        .eq("batalha_id", int(batalha_id))
        .eq("usuario_id", int(user_id))
        .limit(1)
    )
    return bool(res and res.data)
