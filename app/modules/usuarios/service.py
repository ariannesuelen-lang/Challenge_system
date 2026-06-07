from .repository import UsuarioRepository
from .models import UsuarioCreate
from core.exceptions import BadRequestException

class UsuarioService:
    """ Padrão GRASP: Controller / Information Expert """
    def __init__(self):
        self.repo = UsuarioRepository()

    def cadastrar(self, usuario: UsuarioCreate):
        if usuario.tipo_usuario not in ["aluno", "professor"]:
            raise BadRequestException("Tipo de usuário inválido.")
        return self.repo.create(usuario).data[0]

    def listar(self):
        return self.repo.get_all().data