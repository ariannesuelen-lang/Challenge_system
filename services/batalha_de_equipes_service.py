import json
import logging
from database.repositories import BatalhaRepository

logger = logging.getLogger(__name__)

class BatalhaDeEquipesService:
    def __init__(self):
        self.repo = BatalhaRepository()

    def _safe_execute(self, func, *args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res.data if res else []
        except Exception as exc:
            logger.exception("Erro na execução modular do repositório: %s", exc)
            return []

    def listar_times(self):
        return self._safe_execute(self.repo.listar_times)

    def criar_time(self, nome: str) -> bool:
        if not nome or not nome.strip():
            return False
        return self.repo.inserir_time(nome.strip()) is not None

    def editar_time(self, time_id, nome: str) -> bool:
        if not nome or not nome.strip():
            return False
        return self.repo.atualizar_time(int(time_id), nome.strip()) is not None

    def deletar_time(self, time_id) -> bool:
        return self.repo.deletar_time(int(time_id)) is not None

    def listar_membros_time(self, time_id) -> list:
        try:
            res = self.repo.listar_membros_time(int(time_id))
            membros = []
            for r in res.data or []:
                u = r.get("usuarios")
                if isinstance(u, dict) and u.get("id") and u.get("nome"):
                    membros.append({"id": u["id"], "nome": u["nome"], "email": u.get("email", "")})
            return membros
        except Exception:
            return []

    def listar_alunos(self) -> list:
        # Busca usuários centralizados do tipo aluno
        res = self.repo.db.table("usuarios").select("id, nome").eq("tipo_usuario", "aluno").execute()
        return res.data if res else []

    def obter_time_do_aluno(self, user_id) -> int | None:
        try:
            res = self.repo.obter_time_do_estudante(int(user_id))
            if res and res.data:
                return int(res.data[0].get("time_id"))
            return None
        except Exception:
            return None

    def aluno_tem_time(self, user_id) -> bool:
        return self.obter_time_do_aluno(user_id) is not None

    def definir_time_usuario(self, user_id, time_id) -> bool:
        try:
            uid, tid = int(user_id), int(time_id)
            self.repo.deletar_membro_por_usuario(uid)
            return self.repo.inserir_membro_time(tid, uid) is not None
        except Exception:
            return False

    def entrar_no_time(self, time_id, user_id) -> bool:
        if self.aluno_tem_time(user_id):
            return False
        return self.definir_time_usuario(user_id, time_id)

    def adicionar_aluno(self, time_id, user_id) -> bool:
        return self.entrar_no_time(time_id, user_id)

    def remover_aluno(self, time_id, user_id) -> bool:
        try:
            return self.repo.remover_membro_do_time(int(time_id), int(user_id)) is not None
        except Exception:
            return False

    def mover_aluno(self, user_id, time_destino) -> bool:
        return self.definir_time_usuario(user_id, time_destino)

    def listar_batalhas(self) -> list:
        return self._safe_execute(self.repo.listar_batalhas)

    def criar_batalha(self, titulo, descricao, criador_id, quantidade_rodadas=1, tempo_por_rodada=30, criterios=None, regras=None, seguranca=None, prazo=None) -> bool:
        payload = {
            "titulo": titulo.strip(),
            "descricao": descricao.strip() if descricao else "",
            "criador_id": int(criador_id),
            "finalizada": False,
            "quantidade_rodadas": int(quantidade_rodadas),
            "tempo_por_rodada_minutos": int(tempo_por_rodada),
            "criterios_avaliacao": criterios if isinstance(criterios, list) else [],
            "regras_conduta": regras.strip() if regras else "Siga as regras de Fair Play da instituição.",
            "configuracoes_seguranca": seguranca if isinstance(seguranca, dict) else {"bloquear_copia": True, "verificar_plagio": True}
        }
        if prazo:
            payload["prazo"] = str(prazo)
        return self.repo.inserir_batalha(payload) is not None

    def finalizar_batalha(self, batalha_id) -> bool:
        return self.repo.atualizar_status_quiz(int(batalha_id), "finalizada") is not None

    def obter_batalha(self, batalha_id) -> dict | None:
        try:
            res = self.repo.obter_batalha_por_id(int(batalha_id))
            if not res or not res.data:
                return None
            batalha = res.data[0]
            if "criterios_avaliacao" in batalha and isinstance(batalha["criterios_avaliacao"], str):
                batalha["criterios_avaliacao"] = json.loads(batalha["criterios_avaliacao"])
            return batalha
        except Exception:
            return None

    def enviar_resposta_batalha(self, batalha_id, user_id, conteudo) -> tuple[bool, str]:
        batalha = self.obter_batalha(batalha_id)
        if not batalha or batalha.get("finalizada"):
            return False, "Esta batalha já foi encerrada."
        if not conteudo or not str(conteudo).strip():
            return False, "Conteúdo não pode ser vazio."
        
        payload = {"batalha_id": int(batalha_id), "usuario_id": int(user_id), "conteudo": str(conteudo).strip()}
        res = self.repo.inserir_resposta_batalha(payload)
        return res is not None, "Resposta enviada com sucesso."

    def listar_respostas_batalha(self, batalha_id) -> list:
        res = self.repo.listar_respostas_batalha(int(batalha_id))
        return res.data if res else []

    def usuario_ja_respondeu(self, batalha_id, user_id) -> bool:
        res = self.repo.checar_resposta_existente(int(batalha_id), int(user_id))
        return bool(res and res.data)

    def lancar_pontuacao_rodada(self, batalha_id, usuario_id, rodada, pontos_por_criterio) -> bool:
        if not isinstance(pontos_por_criterio, dict):
            return False
        total = sum(pontos_por_criterio.values())
        qtd = len(pontos_por_criterio)
        nota = int(total / qtd) if qtd > 0 else 0

        payload = {
            "batalha_id": int(batalha_id),
            "usuario_id": int(usuario_id),
            "rodada": int(rodada),
            "pontos_criterios": pontos_por_criterio,
            "pontuacao_rodada": nota,
            "tipo_pontuacao": "desafio"
        }
        return self.repo.inserir_pontuacao(payload) is not None

    def calcular_pontuacao_total_aluno(self, batalha_id, usuario_id) -> int:
        res = self.repo.listar_points_aluno(int(batalha_id), int(usuario_id))
        if not res or not res.data:
            return 0
        return sum(row.get("pontuacao_rodada", 0) for row in res.data)

    def obter_ranking_batalha(self, batalha_id) -> list:
        res = self.repo.listar_ranking_batalha(int(batalha_id))
        if not res or not res.data:
            return []
        ranking_dict = {}
        for row in res.data:
            user_id = row.get("usuario_id")
            nome = (row.get("usuarios") or {}).get("nome", "Usuário Desconhecido")
            pontos = row.get("pontuacao_rodada", 0)
            if user_id not in ranking_dict:
                ranking_dict[user_id] = {"nome": nome, "pontuacao_total": 0}
            ranking_dict[user_id]["pontuacao_total"] += pontos
        lista = list(ranking_dict.values())
        lista.sort(key=lambda x: x["pontuacao_total"], reverse=True)
        return lista