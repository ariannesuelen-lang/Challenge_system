from typing import List, Dict, Any
from database.repositories import QuizAoVivoRepository, UsuarioRepository

class QuizAoVivoService:
    def __init__(self):
        self.quiz_repo = QuizAoVivoRepository()
        self.user_repo = UsuarioRepository()

    def _ok(self, dados: Any = None, mensagem: str = None) -> dict:
        res = {"sucesso": True}
        if dados is not None: res["dados"] = dados
        if mensagem: res["mensagem"] = mensagem
        return res

    def _erro(self, mensagem: str) -> dict:
        return {"sucesso": False, "mensagem": mensagem}

    def _verificar_professor(self, usuario_id: int) -> bool:
        u = self.user_repo.db.table("usuarios").select("tipo_usuario").eq("id", usuario_id).execute()
        return bool(u.data and u.data[0].get("tipo_usuario") == "professor")

    def criar_quiz(self, titulo: str, professor_id: int) -> dict:
        if not titulo or len(titulo.strip()) < 3:
            return self._erro("O titulo deve ter pelo menos 3 caracteres.")
        if not self._verificar_professor(professor_id):
            return self._erro("Acesso negado: Usuário não é professor.")
        
        novo = {"titulo": titulo.strip(), "professor_id": professor_id, "status": "pendente"}
        return self._ok(self.quiz_repo.inserir_quiz(novo).data[0])

    def adicionar_pergunta(self, quiz_id: int, professor_id: int, texto: str, alternativas: List[str], indice_correto: int) -> dict:
        if not texto or len(texto.strip()) < 3: return self._erro("Texto inválido.")
        if len(alternativas) < 2: return self._erro("Mínimo 2 alternativas.")
        
        quiz = self.quiz_repo.obter_quiz(quiz_id).data
        if not quiz or quiz[0]["professor_id"] != professor_id:
            return self._erro("Acesso negado.")

        payload = {"quiz_id": quiz_id, "texto": texto.strip(), "alternativas": alternativas, "indice_correto": indice_correto}
        return self._ok(self.quiz_repo.inserir_pergunta(payload).data[0])

    def alterar_status_quiz(self, quiz_id: int, professor_id: int, novo_status: str) -> dict:
        quiz = self.quiz_repo.obter_quiz(quiz_id).data
        if not quiz or quiz[0]["professor_id"] != professor_id: return self._erro("Acesso negado.")
        
        if novo_status == "iniciado":
            pergs = self.quiz_repo.obter_perguntas_quiz(quiz_id).data
            if not pergs: return self._erro("Quiz sem perguntas.")
            return self._ok(self.quiz_repo.iniciar_quiz(quiz_id).data[0])
        
        return self._ok(self.quiz_repo.atualizar_status_quiz(quiz_id, novo_status).data[0])

    def avancar_pergunta(self, quiz_id: int, professor_id: int) -> dict:
        quiz = self.quiz_repo.obter_quiz(quiz_id).data[0]
        if quiz["professor_id"] != professor_id: return self._erro("Acesso negado.")
        
        pergs = self.quiz_repo.obter_perguntas_quiz(quiz_id).data
        atual = int(quiz.get("pergunta_atual") or 0)
        
        if atual + 1 >= len(pergs): return self._erro("Não há próxima pergunta.")
        return self._ok(self.quiz_repo.atualizar_pergunta_atual(quiz_id, atual + 1).data[0])

    def entrar_quiz(self, aluno_id: int, quiz_id: int) -> dict:
        existente = self.quiz_repo.obter_participacao_aluno(aluno_id, quiz_id).data
        if existente: return self._ok(existente[0])
        
        payload = {"quiz_id": quiz_id, "aluno_id": aluno_id, "pontuacao": 0, "finalizou": False}
        return self._ok(self.quiz_repo.inserir_participacao(payload).data[0])

    def obter_pergunta_atual_quiz(self, quiz_id: int) -> dict:
        quiz = self.quiz_repo.obter_quiz(quiz_id).data[0]
        perguntas = self.quiz_repo.obter_perguntas_quiz(quiz_id).data
        atual = quiz.get("pergunta_atual")
        
        if quiz.get("status") != "iniciado" or atual is None:
            return self._ok({"quiz": quiz, "pergunta": None, "fim": False})
            
        idx = int(atual)
        if idx >= len(perguntas): return self._ok({"quiz": quiz, "pergunta": None, "fim": True})
        
        perg = dict(perguntas[idx])
        perg.pop("indice_correto", None) # Remove gabarito por segurança
        return self._ok({"quiz": quiz, "pergunta": perg, "indice": idx, "total": len(perguntas), "fim": False})

    def responder_pergunta(self, participacao_id: int, pergunta_id: int, indice_resposta: int) -> dict:
        part = self.quiz_repo.obter_participacao(participacao_id).data[0]
        perg = self.quiz_repo.obter_pergunta(pergunta_id).data[0]
        
        ja_resp = self.quiz_repo.obter_resposta_aluno(participacao_id, pergunta_id).data
        if ja_resp: return self._erro("Você já respondeu esta pergunta.")
        
        correta = (indice_resposta == perg.get("indice_correto"))
        self.quiz_repo.inserir_resposta({"participacao_id": participacao_id, "pergunta_id": pergunta_id, "indice_resposta": indice_resposta, "correta": correta})
        
        pontos = int(part.get("pontuacao") or 0)
        nova_p = pontos + 10 if correta else pontos
        if correta: self.quiz_repo.atualizar_pontuacao(participacao_id, nova_p)
        
        return self._ok({"correta": correta, "pontuacao": nova_p})

    def obter_ranking(self, quiz_id: int) -> dict:
        return self._ok(self.quiz_repo.obter_ranking(quiz_id).data)