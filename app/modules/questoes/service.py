from .repository import QuestaoRepository
from .models import QuestaoCreate
from uuid import UUID

class QuestaoService:
    def __init__(self):
        self.repo = QuestaoRepository()

    def cadastrar(self, questao: QuestaoCreate):
        db_questao = questao.model_dump(exclude={"alternativas"})
        db_questao["ativo"] = True
        
        res_q = self.repo.create_questao(db_questao)
        questao_id = res_q.data[0]["id"]

        alts_db = [
            {"questao_id": questao_id, "texto": alt.texto, "correta": alt.correta, "ordem_exibicao": alt.ordem_exibicao} 
            for alt in questao.alternativas
        ]
        self.repo.create_alternativas(alts_db)
        return questao_id

    def listar(self): return self.repo.get_all().data
    def filtrar_disciplina(self, disciplina_id: UUID): return self.repo.get_by_disciplina(disciplina_id).data
    def filtrar_nivel(self, nivel: str): return self.repo.get_by_nivel(nivel).data