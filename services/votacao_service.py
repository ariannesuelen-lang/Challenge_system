import streamlit as st
# Correção do caminho de importação baseado no seu repositório real:
from utils.supabase import supabase 

def buscar_voto_usuario(usuario_id, desafio_id):
    """
    Busca se o usuario logado ja votou em algum projeto para este desafio especifico.
    Usa a coluna real 'usuario_id' do seu banco de dados.
    """
    try:
        resultado = supabase.table("votos") \
            .select("*") \
            .eq("usuario_id", str(usuario_id)) \
            .eq("desafio_id", str(desafio_id)) \
            .execute()
        return resultado.data
    except Exception as e:
        print(f"Erro ao buscar voto: {e}")
        return []


def registrar_voto(desafio_id, aluno_id, usuario_id_logado):
    """
    Registra o voto do aluno logado (usuario_id_logado) no projeto do aluno autor (aluno_id)
    dentro do desafio selecionado (desafio_id).
    """
    try:
        # 1. Verifica se o usuário já votou neste desafio
        votos_existentes = buscar_voto_usuario(usuario_id_logado, desafio_id)
        
        if votos_existentes:
            return {
                "sucesso": False,
                "mensagem": "Voce ja registrou um voto para este desafio!"
            }
        
        # 2. Mapeia exatamente as colunas text da tabela public.votos: usuario_id, desafio_id, voto
        dados_voto = {
            "usuario_id": str(usuario_id_logado), # Eleitor
            "desafio_id": str(desafio_id),        # Desafio
            "voto": str(aluno_id)                 # Aluno que recebeu o voto
        }
        
        # 3. Insere o registro no Supabase
        supabase.table("votos").insert(dados_voto).execute()
        
        return {
            "sucesso": True,
            "mensagem": "Voto computado com sucesso!"
        }
        
    except Exception as e:
        return {
            "sucesso": False,
            "mensagem": f"Erro interno ao registrar o voto no banco: {str(e)}"
        }


def listar_votos():
    """
    Retorna a lista completa de votos registrados no sistema (Visão do Professor).
    """
    try:
        resultado = supabase.table("votos").select("*").execute()
        return resultado.data
    except Exception as e:
        print(f"Erro ao listar votos: {e}")
        return []
