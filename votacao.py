import streamlit as st
from supabase import create_client

# =========================
# CONEXÃO COM SUPABASE
# =========================

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

st.set_page_config(page_title="Votação de Desafios", layout="centered")

# Inicializa o estado da página se não existir
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'lista'

# --- FUNÇÕES DE NAVEGAÇÃO ---
def ir_para_votacao():
  st.session_state.pagina = 'votacao'

def ir_para_lista():
  st.session_state.pagina = 'lista'

# --- HEADER ---
col_logo, col_user = st.columns([4, 1])
with col_user:
  st.markdown("👤 *Alunos*")

st.divider()

# --- PÁGINA LISTA ---
if st.session_state.pagina == 'lista':
    
    with st.container(border=True):
      st.write("### Desafio 01 - A Realidade vs. A Teoria")
      st.caption("# em andamento")
        
      if st.button("Acessar Desafio", use_container_width=True):
        ir_para_votacao()
        st.rerun()

# --- PÁGINA VOTAÇÃO ---
elif st.session_state.pagina == 'votacao':

    if st.button("← Voltar para lista"):
      ir_para_lista()
      st.rerun()

    st.divider()
    st.markdown("#### Desafio 01... | *Votação*")
    
    with st.expander("Ver detalhes do Desafio 01", expanded=True):
      st.write("> *Por que isso acontece?*")
      st.write("> Justifique sua resposta com base nos testes realizados.")

    st.divider()
    
    st.write("### Escolha sua nota para a apresentação:")
    
    col1, col2, col3 = st.columns(3)
    with col1:
      bom = st.checkbox("Bom")
    with col2:
      regular = st.checkbox("Regular")
    with col3:
      ruim = st.checkbox("Ruim")

    # =========================
    # ENVIO PARA O BANCO
    # =========================

    if st.button("Enviar Voto", type="primary"):

      if sum([bom, regular, ruim]) > 1:
        st.error("Por favor, selecione apenas uma opção.")

      elif sum([bom, regular, ruim]) == 0:
        st.warning("Selecione uma nota antes de enviar.")

      else:
        voto = "Bom" if bom else "Regular" if regular else "Ruim"

        try:
            supabase.table("votos").insert({
                "usuario": "AlunoTeste",
                "desafio": "Desafio 01",
                "voto": voto
            }).execute()

            st.success(f"Voto '{voto}' enviado com sucesso!")

        except Exception as e:
            st.error(f"Erro ao salvar voto: {e}")
