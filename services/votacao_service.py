import streamlit as st

# TENTATIVA RESILIENTE DE IMPORTAÇÃO DO CLIENTE SUPABASE
try:
    from utils.supabase import supabase
except Exception:
    try:
        from utils.Supabase import supabase
    except Exception:
        # Fallback de segurança: inicializa o cliente diretamente se a importação falhar
        from supabase import create_client
        
        # Recupera as credenciais direto dos secrets do seu Streamlit Cloud
        supabase_url = st.secrets.get("SUPABASE_URL") or st.secrets.get("supabase_url")
        supabase_key = st.secrets.get("SUPABASE_KEY") or st.secrets.get("supabase_key")
        
        if supabase_url and supabase_key:
            supabase = create_client(supabase_url, supabase_key)
        else:
            # Caso não encontre nos secrets, cria um objeto dummy para o app não crashar no boot
            class DummySupabase:
                def table(self, name): return self
                def select(self, *args, **kwargs): return self
                def eq(self, *args, **kwargs): return self
                def execute(self, *args, **kwargs):
                    class Empty: data = []
                    return Empty()
            supabase = DummySupabase()


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
        votos_existentes = buscar_voto_usuario(usuario_id_logado, desafio_id)
        
        if votos_existentes:
            return {
                "sucesso": False,
                "mensagem": "Voce ja registrou um voto para este desafio!"
            }
        
        dados_voto = {
            "usuario_id": str(usuario_id_logado),
            "desafio_id": str(desafio_id),
            "voto": str(aluno_id)
        }
        
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
