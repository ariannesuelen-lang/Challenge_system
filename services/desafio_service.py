import streamlit as st
from utils.supabase import supabase

def listar_desafios():
    """
    Retorna a lista de todos os desafios cadastrados no banco de dados.
    Corrigido para usar a coluna real 'criado_em' em vez de 'data_criacao'.
    """
    try:
        resultado = supabase.table("desafios") \
            .select("*") \
            .order("criado_em", descending=True) \
            .execute()
        return resultado.data
    except Exception as e:
        # Se a ordenacao falhar por algum motivo, tenta uma busca simples sem order
        try:
            resultado = supabase.table("desafios").select("*").execute()
            return resultado.data
        except Exception as erro_critico:
            print(f"Erro critico ao listar desafios: {erro_critico}")
            return []


def criar_desafio(titulo, descricao, criador_id, data_limite=None, nivel_dificuldade="Médio"):
    """
    Cria um novo desafio respeitando as colunas exatas da tabela public.desafios.
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
        return {"sucesso": False, "mensagem": f"Erro ao inserir desafio: {str(e)}"}
