from core.database import Database
from .models import UsuarioCreate
from datetime import datetime

class UsuarioRepository:
    """ Padrão GoF: Repository """
    def __init__(self):
        self.db = Database().get_client()

    def create(self, usuario: UsuarioCreate):
        return self.db.table("usuarios").insert({
            "nome": usuario.nome,
            "email": usuario.email,
            "senha": usuario.senha, 
            "tipo_usuario": usuario.tipo_usuario,
            "matricula": usuario.matricula,
            "turma": usuario.turma,
            "ativo": True,
            "criado_em": datetime.now().isoformat()
        }).execute()

    def get_all(self):
        return self.db.table("usuarios").select("*").execute()