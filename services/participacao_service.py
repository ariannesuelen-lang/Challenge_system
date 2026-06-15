from datetime import datetime
from database.repositories import ParticipacaoRepository

class ParticipacaoService:
    def __init__(self):
        self.repo = ParticipacaoRepository()

    def participar_desafio(self, desafio_id, usuario_id) -> bool:
        existente = self.repo.buscar_participacao(desafio_id, usuario_id)
        if existente.data:
            return False

        self.repo.inserir_participacao({
            "desafio_id": desafio_id,
            "usuario_id": usuario_id,
            "status": "participando"
        })
        return True

    def listar_participantes(self, desafio_id) -> list:
        return self.repo.listar_participantes(desafio_id).data

    def concluir_desafio(self, desafio_id, usuario_id):
        self.repo.atualizar_status_participacao(desafio_id, usuario_id, {
            "status": "concluido",
            "concluido_em": datetime.now().isoformat()
        })
        
        participantes = self.repo.listar_participantes_desafio(desafio_id)
        todos_concluidos = all(p["status"] == "concluido" for p in participantes.data or [])
        
        if todos_concluidos and participantes.data:
            self.repo.atualizar_status_desafio(desafio_id, "concluido")

    def cancelar_participacao(self, desafio_id, usuario_id):
        self.repo.deletar_participacao(desafio_id, usuario_id)