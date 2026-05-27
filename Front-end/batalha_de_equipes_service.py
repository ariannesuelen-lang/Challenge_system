from database.conexao import supabase as banco
from datetime import datetime


# ==========================================
# TIMES
# ==========================================

def criar_time(nome: str, criador_id: int):
    nome = nome.strip() if nome else ""
    if len(nome) < 2:
        return {"sucesso": False, "mensagem": "Nome do time deve ter pelo menos 2 caracteres."}
    try:
        resposta = banco.table("times").insert({
            "nome": nome,
            "criador_id": criador_id,
            "criado_em": datetime.utcnow().isoformat()
        }).execute()
        time_id = resposta.data[0]["id"]
        # Criador entra no time automaticamente como líder
        banco.table("membros_time").insert({
            "time_id": time_id,
            "usuario_id": criador_id,
            "papel": "lider"
        }).execute()
        return {"sucesso": True, "dados": resposta.data[0]}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro: {str(e)}"}


def listar_times():
    try:
        resposta = banco.table("times").select("*").execute()
        return resposta.data
    except Exception:
        return []


def entrar_no_time(time_id: int, usuario_id: int, papel: str = "membro"):
    try:
        # Verificar se já é membro
        existente = banco.table("membros_time").select("id")\
            .eq("time_id", time_id).eq("usuario_id", usuario_id).execute()
        if existente.data:
            return {"sucesso": False, "mensagem": "Você já faz parte deste time."}
        banco.table("membros_time").insert({
            "time_id": time_id,
            "usuario_id": usuario_id,
            "papel": papel
        }).execute()
        return {"sucesso": True}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro: {str(e)}"}


def listar_membros_time(time_id: int):
    try:
        resposta = banco.table("membros_time").select("*, usuarios(nome)")\
            .eq("time_id", time_id).execute()
        return resposta.data
    except Exception:
        return []


def time_do_usuario(usuario_id: int):
    try:
        resposta = banco.table("membros_time").select("*, times(id, nome)")\
            .eq("usuario_id", usuario_id).execute()
        if resposta.data:
            return resposta.data[0]
        return None
    except Exception:
        return None


# ==========================================
# BATALHAS
# ==========================================

def criar_batalha(titulo: str, descricao: str, criador_id: int,
                  time_a_id: int, time_b_id: int, rodadas: int = 3, tempo_rodada: int = 10):
    try:
        resposta = banco.table("batalhas").insert({
            "titulo": titulo.strip(),
            "descricao": descricao.strip(),
            "criador_id": criador_id,
            "time_a_id": time_a_id,
            "time_b_id": time_b_id,
            "rodadas_total": rodadas,
            "tempo_rodada_min": tempo_rodada,
            "status": "aguardando",
            "rodada_atual": 0,
            "criado_em": datetime.utcnow().isoformat()
        }).execute()
        return {"sucesso": True, "dados": resposta.data[0]}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro: {str(e)}"}


def listar_batalhas():
    try:
        resposta = banco.table("batalhas").select(
            "*, times_a:time_a_id(nome), times_b:time_b_id(nome)"
        ).execute()
        return resposta.data
    except Exception:
        return []


def buscar_batalha(batalha_id: int):
    try:
        resposta = banco.table("batalhas").select(
            "*, times_a:time_a_id(id, nome), times_b:time_b_id(id, nome)"
        ).eq("id", batalha_id).single().execute()
        return resposta.data
    except Exception:
        return None


def atualizar_status_batalha(batalha_id: int, status: str, rodada_atual: int = None):
    dados = {"status": status}
    if rodada_atual is not None:
        dados["rodada_atual"] = rodada_atual
    try:
        banco.table("batalhas").update(dados).eq("id", batalha_id).execute()
        return {"sucesso": True}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro: {str(e)}"}


# ==========================================
# PONTUAÇÕES
# ==========================================

def registrar_pontuacao(batalha_id: int, time_id: int, rodada: int, pontos: int, motivo: str = ""):
    try:
        banco.table("pontuacoes_batalha").insert({
            "batalha_id": batalha_id,
            "time_id": time_id,
            "rodada": rodada,
            "pontos": pontos,
            "motivo": motivo,
            "registrado_em": datetime.utcnow().isoformat()
        }).execute()
        return {"sucesso": True}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro: {str(e)}"}


def listar_pontuacoes_batalha(batalha_id: int):
    try:
        resposta = banco.table("pontuacoes_batalha").select("*, times(nome)")\
            .eq("batalha_id", batalha_id).execute()
        return resposta.data
    except Exception:
        return []


def calcular_placar(batalha_id: int, time_a_id: int, time_b_id: int):
    pontuacoes = listar_pontuacoes_batalha(batalha_id)
    pontos_a = sum(p["pontos"] for p in pontuacoes if p["time_id"] == time_a_id)
    pontos_b = sum(p["pontos"] for p in pontuacoes if p["time_id"] == time_b_id)
    return pontos_a, pontos_b


def calcular_mvp(batalha_id: int):
    """Retorna o membro com maior contribuição (mock por ora, pois depende de submissões individuais)"""
    try:
        resposta = banco.table("contribuicoes_batalha").select("*, usuarios(nome)")\
            .eq("batalha_id", batalha_id).order("pontos", desc=True).limit(1).execute()
        if resposta.data:
            return resposta.data[0]
        return None
    except Exception:
        return None
