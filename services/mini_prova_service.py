from database.repositories import AcademicoRepository, UsuarioRepository

class MiniProvaService:
    def __init__(self):
        self.acad_repo = AcademicoRepository()
        self.user_repo = UsuarioRepository()

    def buscar_professor_por_email(self, email: str) -> dict | None:
        usuario = self.user_repo.buscar_por_email(email)
        if usuario and usuario.get("tipo_usuario") in ["professor", "admin"]:
            return usuario
        return None

    def criar_pergunta(self, dados: dict) -> bool:
        professor = self.buscar_professor_por_email(dados["email_professor"])
        if not professor:
            return False

        disciplina = self.acad_repo.buscar_ou_criar_disciplina(dados["disciplina"])
        
        payload_questao = {
            "professor_id": professor["id"],
            "disciplina_id": disciplina["id"],
            "tipo_questao": "multipla_escolha",
            "nivel_dificuldade": dados["nivel"],
            "enunciado": dados["enunciado"],
            "pontos": 1
        }
        questao = self.acad_repo.inserir_questao(payload_questao)
        questao_id = questao.data[0]["id"]

        alternativas = [dados["alternativa_a"], dados["alternativa_b"], dados["alternativa_c"], dados["alternativa_d"], dados["alternativa_e"]]
        letras = ["A", "B", "C", "D", "E"]

        for i in range(5):
            self.acad_repo.inserir_alternativa({
                "questao_id": questao_id,
                "texto": alternativas[i],
                "correta": (letras[i] == dados["resposta_correta"]),
                "ordem_exibicao": i + 1
            })
        return True

    def criar_mini_prova(self, dados: dict) -> list | None:
        professor = self.buscar_professor_por_email(dados["email_professor"])
        if not professor:
            return None

        payload = {
            "professor_id": professor["id"],
            "titulo": dados["titulo"],
            "descricao": dados.get("assunto", ""),
            "quantidade_questoes": dados.get("quantidade_total"),
            "duracao_minutos": dados.get("tempo_minutos"),
            "status": "rascunho"
        }
        try:
            disciplina = self.acad_repo.buscar_ou_criar_disciplina(dados["disciplina"])
            payload["disciplina_id"] = disciplina["id"]
        except Exception:
            pass

        res = self.acad_repo.inserir_mini_prova(payload)
        return res.data

    def listar_mini_provas(self) -> list:
        return self.acad_repo.listar_mini_provas().data

    def listar_perguntas(self) -> list:
        return self.acad_repo.listar_questoes().data

    def buscar_pergunta(self, id_pergunta) -> dict | None:
        res = self.acad_repo.buscar_questao_por_id(id_pergunta)
        return res.data[0] if res.data else None

    def atualizar_pergunta(self, id_pergunta, dados: dict):
        payload = {"enunciado": dados["enunciado"], "nivel_dificuldade": dados["nivel"]}
        self.acad_repo.atualizar_questao(id_pergunta, payload)

    def excluir_pergunta(self, id_pergunta):
        self.acad_repo.excluir_questao(id_pergunta)

    def buscar_mini_prova(self, id_mini_prova) -> dict | None:
        res = self.acad_repo.buscar_mini_prova_por_id(id_mini_prova)
        return res.data[0] if res.data else None

    def atualizar_mini_prova(self, id_mini_prova, dados: dict):
        payload = {}
        for campo, mapa in [("titulo", "titulo"), ("descricao", "descricao"), ("quantidade_questoes", "qtde_questoes"), ("duracao_minutos", "duracao_minutos")]:
            if mapa in dados:
                payload[campo] = dados[mapa]
        if payload:
            self.acad_repo.atualizar_mini_prova(id_mini_prova, payload)

    def excluir_mini_prova(self, id_mini_prova):
        self.acad_repo.excluir_mini_prova(id_mini_prova)