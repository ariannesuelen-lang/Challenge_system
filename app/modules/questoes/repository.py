from uuid import UUID
from core.database import Database
from datetime import datetime

class QuestaoRepository:
    def __init__(self):
        self.db = Database().get_client()

    def create_questao(self, data: dict):
        data["criado_em"] = datetime.now().isoformat()
        return self.db.table("questoes").insert(data).execute()

    def create_alternativas(self, data: list):
        return self.db.table("alternativas").insert(data).execute()

    def get_all(self):
        return self.db.table("questoes").select("*, alternativas(*)").execute()

    def get_by_disciplina(self, disciplina_id: UUID):
        return self.db.table("questoes").select("*").eq("disciplina_id", str(disciplina_id)).execute()

    def get_by_nivel(self, nivel: str):
        return self.db.table("questoes").select("*").eq("nivel_dificuldade", nivel).execute()