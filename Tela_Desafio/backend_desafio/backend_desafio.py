import os
from supabase import create_client, Client
from datetime import date

# ==========================================
# 1. CONEXÃO COM O BANCO DE DADOS
# ==========================================
# SUBSTITUA PELAS SUAS CHAVES REAIS DO SUPABASE
# Exemplo de URL correta: "https://abcdefghijk.supabase.co" (Sem barra no final!)
SUPABASE_URL = "SUPABASE_URL"
SUPABASE_KEY = "SUPABASE_KEY"

banco: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# 2. FUNÇÕES DO BANCO (CRUD)
# ==========================================

# ... (mantenha os seus imports e a conexão com o banco iguais) ...

def criar_desafio(titulo: str, descricao: str, criador_id: int, disciplina_id: int, data_limite: date, data_criacao: date = None):
    # ==========================================
    # 1. VALIDAÇÕES (O Guarda-Costas)
    # ==========================================
    
    # Remove espaços vazios do começo e do fim
    titulo = titulo.strip() if titulo else ""
    descricao = descricao.strip() if descricao else ""

    if len(titulo) < 3:
        return {"sucesso": False, "mensagem": "O título deve ter pelo menos 3 caracteres."}
    
    if len(descricao) > 500:
        return {"sucesso": False, "mensagem": "A descrição é muito longa (máximo 500 caracteres)."}
        
    if criador_id <= 0:
        return {"sucesso": False, "mensagem": "O ID do criador deve ser um número válido e maior que zero."}
        
    if disciplina_id <= 0:
        return {"sucesso": False, "mensagem": "O ID da disciplina deve ser um número válido e maior que zero."}
        
    if data_limite < date.today():
        return {"sucesso": False, "mensagem": "A data limite não pode ser no passado."}

    # ==========================================
    # 2. SE TUDO ESTIVER CERTO, SALVA NO BANCO
    # ==========================================
    if not data_criacao:
        data_criacao = date.today()
        
    novo_desafio = {
        "titulo": titulo,
        "descricao": descricao,
        "criador_id": criador_id,
        "disciplina_id": disciplina_id,
        "data_criacao": f"{data_criacao}T00:00:00Z", 
        "data_limite": f"{data_limite}T23:59:59Z"
    }
    
    try:
        # Tenta inserir no banco
        resposta = banco.table("desafios").insert(novo_desafio).execute()
        # Retorna o status de sucesso e os dados que foram salvos
        return {"sucesso": True, "dados": resposta.data}
    except Exception as e:
        # Se o banco recusar por algum motivo (ex: o banco caiu), capturamos o erro
        return {"sucesso": False, "mensagem": f"Erro interno no banco de dados: {str(e)}"}

# ... (pode manter as funções listar, atualizar e deletar como estão por enquanto) ...

def listar_desafios():
    resposta = banco.table("desafios").select("*").execute()
    return resposta.data

def atualizar_desafio(id_desafio: int, dados_atualizados: dict):
    resposta = banco.table("desafios").update(dados_atualizados).eq("id", id_desafio).execute()
    return resposta.data

def deletar_desafio(id_desafio: int):
    resposta = banco.table("desafios").delete().eq("id", id_desafio).execute()
    return resposta.data