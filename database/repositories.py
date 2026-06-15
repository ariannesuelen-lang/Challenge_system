# database/repositories.py
from database import obter_client_banco

class BaseRepository:
    """Injeta a conexão única do Supabase em todos os repositórios"""
    def __init__(self):
        self.db = obter_client_banco()

class UsuarioRepository(BaseRepository):
    def buscar_por_email(self, email: str):
        res = self.db.table("usuarios").select("*").eq("email", email).execute()
        return res.data[0] if res.data else None

    def verificar_existencia_email(self, email: str):
        res = self.db.table("usuarios").select("id").eq("email", email).execute()
        return len(res.data) > 0

    def inserir_usuario(self, payload: dict):
        return self.db.table("usuarios").insert(payload).execute()

    def inserir_professor_legado(self, payload: dict):
        return self.db.table("professores").insert(payload).execute()

    def inserir_aluno_legado(self, payload: dict):
        return self.db.table("alunos").insert(payload).execute()

class BatalhaRepository(BaseRepository):
    def listar_times(self):
        return self.db.table("times").select("*").order("id").execute()

    def inserir_time(self, nome: str):
        return self.db.table("times").insert({"nome": nome}).execute()

    def atualizar_time(self, time_id: int, nome: str):
        return self.db.table("times").update({"nome": nome}).eq("id", time_id).execute()

    def deletar_time(self, time_id: int):
        return self.db.table("times").delete().eq("id", time_id).execute()

    def listar_membros_time(self, time_id: int):
        return self.db.table("time_membros").select("usuario_id, usuarios(id, nome, email)").eq("time_id", time_id).execute()

    def deletar_membro_por_usuario(self, usuario_id: int):
        return self.db.table("time_membros").delete().eq("usuario_id", usuario_id).execute()

    def inserir_membro_time(self, time_id: int, usuario_id: int):
        return self.db.table("time_membros").insert({"time_id": time_id, "usuario_id": usuario_id}).execute()

    def remover_membro_do_time(self, time_id: int, usuario_id: int):
        return self.db.table("time_membros").delete().eq("time_id", time_id).eq("usuario_id", usuario_id).execute()

    def obter_time_do_estudante(self, usuario_id: int):
        return self.db.table("time_membros").select("time_id").eq("usuario_id", usuario_id).limit(1).execute()

    def listar_batalhas(self):
        return self.db.table("batalhas").select("*").order("id").execute()

    def inserir_batalha(self, payload: dict):
        return self.db.table("batalhas").insert(payload).execute()

    def atualizar_status_batalha(self, batalha_id: int, payload: dict):
        return self.db.table("batalhas").update(payload).eq("id", batalha_id).execute()

    def obter_batalha_por_id(self, batalha_id: int):
        return self.db.table("batalhas").select("*").eq("id", batalha_id).limit(1).execute()

    def inserir_resposta_batalha(self, payload: dict):
        return self.db.table("respostas_batalha").insert(payload).execute()

    def listar_respostas_batalha(self, batalha_id: int):
        return self.db.table("respostas_batalha").select("*, usuarios(nome)").eq("batalha_id", batalha_id).order("criado_em").execute()

    def checar_resposta_existente(self, batalha_id: int, usuario_id: int):
        return self.db.table("respostas_batalha").select("id").eq("batalha_id", batalha_id).eq("usuario_id", usuario_id).limit(1).execute()

    def inserir_pontuacao(self, payload: dict):
        return self.db.table("pontuacoes").insert(payload).execute()

    def listar_pontos_aluno(self, batalha_id: int, usuario_id: int):
        return self.db.table("pontuacoes").select("pontuacao_rodada").eq("batalha_id", batalha_id).eq("usuario_id", usuario_id).execute()

    def listar_ranking_batalha(self, batalha_id: int):
        return self.db.table("pontuacoes").select("usuario_id, pontuacao_rodada, usuarios(nome)").eq("batalha_id", batalha_id).execute()

class DesafioRepository(BaseRepository):
    def listar_desafios(self):
        return self.db.table("desafios").select("*").order("criado_em", descending=True).execute()

    def inserir_desafio(self, payload: dict):
        return self.db.table("desafios").insert(payload).execute()

class AcademicoRepository(BaseRepository):
    def buscar_ou_criar_disciplina(self, nome: str):
        buscar = self.db.table("disciplinas").select("*").eq("nome", nome).execute()
        if buscar.data:
            return buscar.data[0]
        criar = self.db.table("disciplinas").insert({"nome": nome}).execute()
        return criar.data[0]

    def inserir_questao(self, payload: dict):
        return self.db.table("questoes").insert(payload).execute()

    def inserir_alternativa(self, payload: dict):
        return self.db.table("alternativas").insert(payload).execute()

    def inserir_mini_prova(self, payload: dict):
        return self.db.table("mini_provas").insert(payload).execute()

    def listar_mini_provas(self):
        return self.db.table("mini_provas").select("*").execute()

    def listar_questoes(self):
        return self.db.table("questoes").select("*").execute()

    def buscar_questao_por_id(self, questao_id: str):
        return self.db.table("questoes").select("*").eq("id", questao_id).limit(1).execute()

    def atualizar_questao(self, questao_id: str, payload: dict):
        return self.db.table("questoes").update(payload).eq("id", questao_id).execute()

    def excluir_questao(self, questao_id: str):
        return self.db.table("questoes").delete().eq("id", questao_id).execute()

    def buscar_mini_prova_por_id(self, prova_id: str):
        return self.db.table("mini_provas").select("*").eq("id", prova_id).limit(1).execute()

    def atualizar_mini_prova(self, prova_id: str, payload: dict):
        return self.db.table("mini_provas").update(payload).eq("id", prova_id).execute()

    def excluir_mini_prova(self, prova_id: str):
        return self.db.table("mini_provas").delete().eq("id", prova_id).execute()

class ParticipacaoRepository(BaseRepository):
    def buscar_participacao(self, desafio_id: str, usuario_id: int):
        return self.db.table("participantes_desafio").select("*").eq("desafio_id", desafio_id).eq("usuario_id", usuario_id).execute()

    def inserir_participacao(self, payload: dict):
        return self.db.table("participantes_desafio").insert(payload).execute()

    def listar_participantes(self, desafio_id: str):
        return self.db.table("participantes_desafio").select("*, usuarios(nome)").eq("desafio_id", desafio_id).execute()

    def atualizar_status_participacao(self, desafio_id: str, usuario_id: int, payload: dict):
        return self.db.table("participantes_desafio").update(payload).eq("desafio_id", desafio_id).eq("usuario_id", usuario_id).execute()

    def listar_participantes_desafio(self, desafio_id: str):
        return self.db.table("participantes_desafio").select("*").eq("desafio_id", desafio_id).execute()

    def atualizar_status_desafio(self, desafio_id: str, status: str):
        return self.db.table("desafios").update({"status": status}).eq("id", desafio_id).execute()

    def deletar_participacao(self, desafio_id: str, usuario_id: int):
        return self.db.table("participantes_desafio").delete().eq("desafio_id", desafio_id).eq("usuario_id", usuario_id).execute()

class QuizAoVivoRepository(BaseRepository):
    def inserir_quiz(self, dados: dict):
        return self.db.table("quizzes").insert(dados).execute()

    def obter_quiz(self, quiz_id: int):
        return self.db.table("quizzes").select("*").eq("id", quiz_id).limit(1).execute()

    def atualizar_status_quiz(self, quiz_id: int, status: str):
        return self.db.table("quizzes").update({"status": status}).eq("id", quiz_id).execute()

    def atualizar_pergunta_atual(self, quiz_id: int, pergunta_atual: int):
        return self.db.table("quizzes").update({"pergunta_atual": pergunta_atual}).eq("id", quiz_id).execute()

    def iniciar_quiz(self, quiz_id: int):
        return self.db.table("quizzes").update({"status": "iniciado", "pergunta_atual": 0}).eq("id", quiz_id).execute()

    def inserir_pergunta(self, dados: dict):
        return self.db.table("perguntas_quizaovivo").insert(dados).execute()

    def obter_pergunta(self, pergunta_id: int):
        return self.db.table("perguntas_quizaovivo").select("*").eq("id", pergunta_id).limit(1).execute()

    def obter_perguntas_quiz(self, quiz_id: int):
        return self.db.table("perguntas_quizaovivo").select("*").eq("quiz_id", quiz_id).order("id").execute()

    def inserir_participacao(self, dados: dict):
        return self.db.table("participacao_quizaovivo").insert(dados).execute()

    def obter_participacao(self, participacao_id: int):
        return self.db.table("participacao_quizaovivo").select("*").eq("id", participacao_id).limit(1).execute()

    def obter_participacao_aluno(self, aluno_id: int, quiz_id: int):
        return self.db.table("participacao_quizaovivo").select("*").eq("aluno_id", aluno_id).eq("quiz_id", quiz_id).limit(1).execute()

    def atualizar_pontuacao(self, participacao_id: int, pontos: int):
        return self.db.table("participacao_quizaovivo").update({"pontuacao": pontos}).eq("id", participacao_id).execute()

    def inserir_resposta(self, dados: dict):
        return self.db.table("respostas_quizaovivo").insert(dados).execute()

    def obter_resposta_aluno(self, participacao_id: int, pergunta_id: int):
        return self.db.table("respostas_quizaovivo").select("*").eq("participacao_id", participacao_id).eq("pergunta_id", pergunta_id).limit(1).execute()

    def obter_ranking(self, quiz_id: int):
        return self.db.table("participacao_quizaovivo").select("pontuacao, usuarios(nome)").eq("quiz_id", quiz_id).order("pontuacao", desc=True).execute()

class VotacaoRepository(BaseRepository):
    def buscar_voto_existente(self, usuario_id: int, desafio_id: str):
        return self.db.table("votos").select("*").eq("usuario_id", str(usuario_id)).eq("desafio_id", str(desafio_id)).execute()

    def inserir_voto(self, payload: dict):
        return self.db.table("votos").insert(payload).execute()

    def listar_todos_votos(self):
        return self.db.table("votos").select("*").execute()