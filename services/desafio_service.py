import streamlit as st

# Importacao tolerante a falhas do cliente Supabase
try:
    from utils.supabase import supabase
except Exception:
    try:
        from utils.Supabase import supabase
    except Exception:
        try:
            from supabase_config import supabase
        except Exception:
            try:
                from supabase import create_client
                supabase_url = st.secrets.get("SUPABASE_URL") or st.secrets.get("supabase_url")
                supabase_key = st.secrets.get("SUPABASE_KEY") or st.secrets.get("supabase_key")
                if supabase_url and supabase_key:
                    supabase = create_client(supabase_url, supabase_key)
                else:
                    raise ValueError("Credenciais nao encontradas.")
            except Exception:
                class DummySupabase:
                    def table(self, name): return self
                    def select(self, *args, **kwargs): return self
                    def order(self, *args, **kwargs): return self
                    def execute(self, *args, **kwargs):
                        class Empty: data = []
                        return Empty()
                supabase = DummySupabase()


def listar_desafios():
    """
    Retorna a lista de todos os desafios cadastrados.
    Usa a coluna correta criado_em mapeada do PostgreSQL.
    """
    try:
        resultado = supabase.table("desafios") \
            .select("*") \
            .order("criado_em", descending=True) \
            .execute()
        return resultado.data
    except Exception as e:
        try:
            resultado = supabase.table("desafios").select("*").execute()
            return resultado.data
        except Exception as erro_critico:
            print(f"Erro critico ao listar desafios: {erro_critico}")
            return []


def criar_desafio(titulo, descricao, criador_id, data_limite=None, nivel_dificuldade="Medio"):
    """
    Insere um novo desafio respeitando o esquema oficial do banco de dados.
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
