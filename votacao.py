import streamlit as st

st.set_page_config(page_title="Votação de Desafios", layout="centered")

# Inicializa o estado da página se não existir
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'lista'

# --- FUNÇÕES DE NAVEGAÇÃO ---
def ir_para_votacao():
  st.session_state.pagina = 'votacao'
def ir_para_lista():
  st.session_state.pagina = 'lista'

# --- HEADER (Comum às duas páginas) ---
col_logo, col_user = st.columns([4, 1])
with col_user:
  st.markdown("👤 *Aluno*")
st.divider()

# --- PÁGINA 01: LISTA DE DESAFIOS ---
if st.session_state.pagina == 'lista':
    
    # Container do Desafio
    with st.container(border=True):
      st.write("### Desafio 01 - A Realidade vs. A Teoria")
      st.caption("# em andamento")
        
      if st.button("Acessar Desafio", use_container_width=True):
        ir_para_votacao()
        st.rerun()

# --- PÁGINA 02: VOTAÇÃO ---
elif st.session_state.pagina == 'votacao':
    if st.button("← Voltar para lista"):
      ir_para_lista()
      st.rerun()
    st.divider()
    st.markdown("#### Desafio 01... | *Votação*")
    
    # Detalhes do Desafio
    with st.expander("Ver detalhes do Desafio 01", expanded=True):
      st.write("> *Por que isso acontece?*")
      st.write("> Justifique sua resposta com base nos testes realizados.")
    st.divider()
    
    # Área de Votação
    st.write("### Escolha sua nota para a apresentação:")
    
    # Criando os checkboxes lado a lado
    col1, col2, col3 = st.columns(3)
    with col1:
      bom = st.checkbox("Bom")
    with col2:
      regular = st.checkbox("Regular")
    with col3:
      ruim = st.checkbox("Ruim")

    # Botão para confirmar o voto (importante ao usar checkbox)
    if st.button("Enviar Voto", type="primary"):
      if sum([bom, regular, ruim]) > 1:
        st.error("Por favor, selecione apenas uma opção.")
      elif sum([bom, regular, ruim]) == 0:
        st.warning("Selecione uma nota antes de enviar.")
      else:
        voto = "Bom" if bom else "Regular" if regular else "Ruim"
        st.success(f"Voto '{voto}' enviado com sucesso!")
