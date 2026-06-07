from uuid import UUID
from core.database import Database

class MiniProvaRepository:
    def __init__(self):
        self.db = Database().get_client()

    def get_prova(self, prova_id: UUID):
        return self.db.table("mini_provas").select("*").eq("id", str(prova_id)).single().execute()

    def get_questoes_da_disciplina(self, disciplina_id: UUID, limit: int):
        return self.db.table("questoes").select("*, alternativas(*)").eq("disciplina_id", str(disciplina_id)).eq("ativo", True).limit(limit).execute()

    def get_alternativa_correta(self, questao_id: UUID):
        return self.db.table("alternativas").select("*").eq("questao_id", str(questao_id)).eq("correta", True).single().execute()

    def get_pontos_questao(self, questao_id: UUID):
        return self.db.table("questoes").select("pontos").eq("id", str(questao_id)).single().execute()

    def salvar_resposta(self, data: dict):
        return self.db.table("respostas_mini_provas").insert(data).execute()