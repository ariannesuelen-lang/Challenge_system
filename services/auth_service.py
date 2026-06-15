import hashlib
import re
from database.repositories import UsuarioRepository

class AuthService:
    def __init__(self):
        self.user_repo = UsuarioRepository()

    def criptografar_senha(self, senha: str) -> str:
        return hashlib.sha256(senha.encode()).hexdigest()

    def senha_valida(self, senha: str) -> str:
        if len(senha) < 8:
            return "A senha deve ter no mínimo 8 caracteres"
        if not re.search(r"[A-Z]", senha):
            return "A senha deve conter letra maiúscula"
        if not re.search(r"\d", senha):
            return "A senha deve conter número"
        return "ok"

    def login_usuario(self, email: str, senha: str) -> dict | None:
        usuario = self.user_repo.buscar_por_email(email)
        if usuario and usuario.get("senha") == self.criptografar_senha(senha):
            return usuario
        return None

    def cadastrar_usuario(self, nome: str, email: str, tipo_usuario: str, senha: str) -> str:
        try:
            validar = self.senha_valida(senha)
            if validar != "ok":
                return validar

            if self.user_repo.verificar_existencia_email(email):
                return "E-mail já cadastrado"

            payload = {
                "nome": nome,
                "email": email,
                "tipo_usuario": tipo_usuario,
                "senha": self.criptografar_senha(senha)
            }
            self.user_repo.inserir_usuario(payload)

            # Sincroniza tabelas legadas se existirem
            if tipo_usuario == "professor":
                self.user_repo.inserir_professor_legado({"nome": nome, "email": email})
            elif tipo_usuario == "aluno":
                self.user_repo.inserir_aluno_legado({"nome": nome, "email": email})

            return "ok"
        except Exception as erro:
            return f"Erro ao cadastrar usuário: {erro}"