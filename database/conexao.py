import os
import streamlit as st
from supabase import create_client

# Tenta st.secrets primeiro (Streamlit Cloud)
# Se nao encontrar, usa variaveis de ambiente / .env (local)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
except Exception:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise Exception(
        "Credenciais do Supabase nao encontradas. "
        "Configure SUPABASE_URL e SUPABASE_KEY em st.secrets ou no arquivo .env"
    )

supabase = create_client(url, key)
