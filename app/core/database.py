import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class Database:
    """
    Classe Singleton para gerenciar a conexão com o banco de dados Supabase.
    Utiliza variáveis de ambiente para configurar a URL e a chave de acesso.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.client = create_client(url, key)
        return cls._instance

    def get_client(self) -> Client:
        return self.client