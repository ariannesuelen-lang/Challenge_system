from supabase import create_client
import pandas as pd

# =========================
# CONEXÃO COM SUPABASE
# =========================

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

def inserir_voto(usuario, desafio, voto):
    return supabase.table("votos").insert({
        "usuario": usuario,
        "desafio": desafio,
        "voto": voto
    }).execute()

def listar_votos():
    return supabase.table("votos").select("*").execute()

def buscar_votos_por_desafio(desafio):
    return supabase.table("votos").select("*").eq("desafio", desafio).execute()

def buscar_voto_por_id(id):
    return supabase.table("votos").select("*").eq("id", id).execute()

def atualizar_voto(id, novo_voto):
    return supabase.table("votos").update({
        "voto": novo_voto
    }).eq("id", id).execute()

def deletar_voto(id):
    return supabase.table("votos").delete().eq("id", id).execute()
