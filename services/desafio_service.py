from database.repositories import DesafioRepository

class DesafioService:
    def __init__(self):
        self.repo = DesafioRepository()

    def listar_desafios(self) -> list:
        try:
            res = self.repo.listar_desafios()
            return res.data if res else []
        except Exception:
            return []

    def criar_desafio(self, titulo: str, descricao: str, criador_id: int, data_limite=None, nivel_dificuldade="Medio") -> dict:
        try:
            dados = {
                "titulo": str(titulo),
                "descricao": str(descricao),
                "criador_id": int(criador_id),
                "nivel_dificuldade": str(nivel_dificuldade)
            }
            if data_limite:
                dados["data_limite"] = str(data_limite)
            res = self.repo.inserir_desafio(dados)
            return {"sucesso": True, "dados": res.data}
        except Exception as e:
            return {"sucesso": False, "mensagem": f"Erro ao criar desafio: {str(e)}"}