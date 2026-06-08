import streamlit as st
from utils.supabase import supabase

def listar_desafios():
    """
    Retorna a lista de todos os desafios cadastrados.
    Usa a coluna correta 'criado_em' mapeada do PostgreSQL.
    """
    try:
        resultado = supabase.table("desafios") \
            .select("*") \
            .order("criado_em", descending=True) \
            .execute()
        return resultado.data
    except Exception as e:
        # Fallback caso o cache do cache do PostgREST reclame da ordenação
        try:
            resultado = supabase.table("desafios").select("*").execute()
            return resultado.data
        except Exception as erro_critico:
            print(f"Erro critico ao listar desafios: {erro_critico}")
            return []

def criar_desafio(titulo, descricao, criador_id, data_limite=None, nivel_dificuldade="Médio"):
    """
    Insere um novo desafio respeitando o esquema oficial do banco.
    """
    try:
        dados = {
            "titulo": str(titulo),
            "descricao": str(descricao),
            "criador_id": int(criador_id),
            "nivel_dificuldade": str(nivel_dificuldade)
        }
        if data_limite:
            dados["data_limite"] = str(data_limite)
            
        resultado = supabase.table("desafios").insert(dados).execute()
        return {"sucesso": True, "dados": resultado.data}
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Erro ao criar desafio: {str(e)}"}
