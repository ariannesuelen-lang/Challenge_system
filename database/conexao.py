import os
import logging
import streamlit as st
from supabase import create_client, Client

logger = logging.getLogger(__name__)

# Mantém o suporte ao arquivo .env para desenvolvimento local fora do Streamlit se necessário
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class SupabaseConnection:
    """Classe responsável pelo gerenciamento da conexão única (Singleton) com o Supabase."""
    
    _instance: Client = None

    @classmethod
    def get_client(cls) -> Client:
        """
        Retorna a instância única do cliente do Supabase. 
        Se ela não existir, faz a leitura segura das credenciais e inicializa.
        """
        if cls._instance is None:
            try:
                # Tenta ler do secrets do Streamlit primeiro
                url = st.secrets["SUPABASE_URL"]
                key = st.secrets["SUPABASE_KEY"]
            except Exception:
                # Fallback para variáveis de ambiente locais (.env / OS)
                url = os.getenv("SUPABASE_URL")
                key = os.getenv("SUPABASE_KEY")

            if not url or not key:
                logger.error("Credenciais do Supabase não foram encontradas no sistema.")
                raise RuntimeError(
                    "Credenciais do Supabase não encontradas. "
                    "Configure SUPABASE_URL e SUPABASE_KEY em .streamlit/secrets.toml ou no arquivo .env"
                )

            # Inicializa a instância única
            cls._instance = create_client(url, key)
            logger.info("Instância do cliente Supabase inicializada com sucesso (Singleton).")
            
        return cls._instance