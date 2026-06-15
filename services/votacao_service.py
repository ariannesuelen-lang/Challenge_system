from database.repositories import VotacaoRepository

class VotacaoService:
    def __init__(self):
        self.repo = VotacaoRepository()

    def buscar_voto_usuario(self, usuario_id, desafio_id) -> list:
        try:
            res = self.repo.buscar_voto_existente(usuario_id, desafio_id)
            return res.data or []
        except Exception:
            return []

    def registrar_voto(self, desafio_id, aluno_id, usuario_id_logado) -> dict:
        try:
            votos = self.buscar_voto_usuario(usuario_id_logado, desafio_id)
            if votos:
                return {"sucesso": False, "mensagem": "Você já registrou um voto para este desafio!"}

            payload = {
                "usuario_id": str(usuario_id_logado),
                "desafio_id": str(desafio_id),
                "voto": str(aluno_id)
            }
            self.repo.inserir_voto(payload)
            return {"sucesso": True, "mensagem": "Voto computado com sucesso!"}
        except Exception as e:
            return {"sucesso": False, "mensagem": f"Erro interno no banco: {e}"}

    def listar_votos(self) -> list:
        res = self.repo.listar_todos_votos()
        return res.data if res else []