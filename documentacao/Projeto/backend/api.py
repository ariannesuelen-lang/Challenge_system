from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class CadastroSchema(BaseModel):
    email: EmailStr
    password: str
    nome: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

@app.get("/")
def home():
    return {"status": "API Online"}

@app.post("/signup")
def signup(dados: CadastroSchema):
    try:
        auth_response = supabase.auth.sign_up({
            "email": dados.email,
            "password": dados.password
        })

        if auth_response.user:
            user_id = auth_response.user.id
            supabase.table("usuarios").insert({
                "id": user_id, 
                "nome": dados.nome, 
                "email": dados.email
            }).execute()

            return {"mensagem": "Sucesso", "user_id": user_id}
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/login")
def login(dados: LoginSchema):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": dados.email,
            "password": dados.password
        })
        
        return {
            "access_token": response.session.access_token,
            "user": response.user
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Incorreto")
