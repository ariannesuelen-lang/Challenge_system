import json
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
    for r in res.data or []:
        if not isinstance(r, dict):
            continue
        u = r.get("usuarios")
        if not isinstance(u, dict):
            continue
        if u.get("id") and u.get("nome"):
            membros.append(
                {"id": u["id"], "nome": u["nome"], "email": u.get("email", "")}
            )
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
        supabase.table("time_membros").insert(
            {"time_id": time_id, "usuario_id": user_id}
        )
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


def criar_batalha(
    titulo,
    descricao,
    criador_id,
    quantidade_rodadas=1,
    tempo_por_rodada=30,
    criterios=None,
    regras=None,
    seguranca=None,
    prazo=None,
):
    config_seguranca = (
        seguranca
        if isinstance(seguranca, dict)
        else {"bloquear_copia": True, "verificar_plagio": True, "limitar_IP": False}
    )

    payload = {
        "titulo": titulo.strip(),
        "descricao": descricao.strip() if descricao else "",
        "criador_id": int(criador_id),
        "finalizada": False,
        "quantidade_rodadas": int(quantidade_rodadas),
        "tempo_por_rodada_minutos": int(tempo_por_rodada),
        "criterios_avaliacao": criterios if isinstance(criterios, list) else [],
        "regras_conduta": (
            regras.strip()
            if  regras
            else "Siga as regras de Fair Play da instituição."
        ),
        "configuracoes_seguranca": config_seguranca,
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

    batalha = res.data[0]

    if "criterios_avaliacao" in batalha and isinstance(
        batalha["criterios_avaliacao"], str
    ):
        try:
            batalha["criterios_avaliacao"] = json.loads(
                batalha["criterios_avaliacao"]
            )
        except Exception:
            batalha["criterios_avaliacao"] = []

    return batalha


# --------------------------------------------------
# RESPOSTAS DE BATALHA
# --------------------------------------------------


def enviar_resposta_batalha(batalha_id, user_id, conteudo):
    batalha = obter_batalha(batalha_id)
    if not batalha or batalha.get("finalizada"):
        return False, "Esta batalha já foi encerrada."

    if not conteudo or not str(conteudo).strip():
        return False, "Conteúdo não pode ser vazio."

    res = _execute(
        supabase.table("respostas_batalha").insert(
            {
                "batalha_id": int(batalha_id),
                "usuario_id": int(user_id),
                "conteudo": str(conteudo).strip(),
            }
        )
    )
    return res is not None, "Resposta enviada com sucesso."


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


# --------------------------------------------------
# PONTUAÇÃO E RANKING
# --------------------------------------------------


def lancar_pontuacao_rodada(batalha_id, usuario_id, rodada, pontos_por_criterio):
    if not isinstance(pontos_por_criterio, dict):
        return False

    total_pontos = sum(pontos_por_criterio.values())
    qtd_criterios = len(pontos_por_criterio)
    nota_rodada = int(total_pontos / qtd_criterios) if qtd_criterios > 0 else 0

    payload = {
        "batalha_id": int(batalha_id),
        "usuario_id": int(usuario_id),
        "rodada": int(rodada),
        "pontos_criterios": pontos_por_criterio,
        "pontuacao_rodada": nota_rodada,
    }

    res = _execute(supabase.table("pontuacoes").insert(payload))
    return res is not None


def calcular_pontuacao_total_aluno(batalha_id, usuario_id):
    res = _execute(
        supabase.table("pontuacoes")
        .select("pontuacao_rodada")
        .eq("batalha_id", int(batalha_id))
        .eq("usuario_id", int(usuario_id))
    )

    if not res or not res.data:
        return 0

    return sum(row.get("pontuacao_rodada", 0) for row in res.data)


def obter_ranking_batalha(batalha_id):
    res = _execute(
        supabase.table("pontuacoes")
        .select("usuario_id, pontuacao_rodada, usuarios(nome)")
        .eq("batalha_id", int(batalha_id))
    )

    if not res or not res.data:
        return []

    ranking_dict = {}
    for row in res.data:
        user_id = row.get("usuario_id")
        user_info = row.get("usuarios") or {}
        nome_usuario = user_info.get("nome", "Usuário Desconhecido")
        pontos = row.get("pontuacao_rodada", 0)

        if user_id not in ranking_dict:
            ranking_dict[user_id] = {"nome": nome_usuario, "pontuacao_total": 0}

        ranking_dict[user_id]["pontuacao_total"] += pontos

    lista_ranking = list(ranking_dict.values())
    lista_ranking.sort(key=lambda x: x["pontuacao_total"], reverse=True)

    return lista_ranking


# --------------------------------------------------
# MODERAÇÃO E CONTROLE (MODO MODERADOR)
# --------------------------------------------------


def alterar_status_batalha(batalha_id, novo_status):
    if novo_status not in ["ativa", "pausada", "finalizada"]:
        return False

    payload = {"status": novo_status}
    if novo_status == "finalizada":
        payload["finalizada"] = True
    elif novo_status == "ativa":
        payload["finalizada"] = False

    res = _execute(
        supabase.table("batalhas")
        .update(payload)
        .eq("id", int(batalha_id))
    )
    return res is not None


def aplicar_penalidade_aluno(batalha_id, usuario_id, pontos_deduzidos, motivo):
    batalha = obter_batalha(batalha_id)
    if not batalha:
        return False

    historico_penalidades = batalha.get("penalidades") or []
    if isinstance(historico_penalidades, str):
        try:
            historico_penalidades = json.loads(historico_penalidades)
        except Exception:
            historico_penalidades = []

    nova_penalidade = {
        "usuario_id": int(usuario_id),
        "pontos_deduzidos": int(pontos_deduzidos),
        "motivo": motivo.strip() if motivo else "Sem motivo especificado",
        "timestamp": "now()", 
    }
    historico_penalidades.append(nova_penalidade)

    _execute(
        supabase.table("batalhas")
        .update({"penalidades": historico_penalidades})
        .eq("id", int(batalha_id))
    )

    payload_ponto = {
        "batalha_id": int(batalha_id),
        "usuario_id": int(usuario_id),
        "rodada": 99,
        "pontos_criterios": {"Penalidade": -int(pontos_deduzidos)},
        "pontuacao_rodada": -int(pontos_deduzidos),
    }

    res = _execute(supabase.table("pontuacoes").insert(payload_ponto))
    return res is not None
