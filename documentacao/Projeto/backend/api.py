from fastapi import FastAPI
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

@app.get("/")
def home():
    return {"status": "API Online"}

@app.get("/usuarios")
def buscar_usuarios():
    response = supabase.table("sua_tabela").select("*").execute()
    return response.data

@app.post("/cadastrar")
def cadastrar(dados: dict):
    response = supabase.table("sua_tabela").insert(dados).execute()
    return {"mensagem": "Salvo com sucesso!", "dados": response.data}
