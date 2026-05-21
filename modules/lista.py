import streamlit as st
from modules.utils import ir
from conexao import listar_desafios

def render():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write("### Desafios Ativos")
    with col2:
        # Botão para ir para a página de gerenciamento
        if st.button("⚙️ Admin", key="btn_admin"):
            ir('admin_desafios')

    # Busca os desafios do Supabase
    resposta = listar_desafios()
    desafios = resposta.data if resposta.data else []

    if not desafios:
        st.info("Nenhum desafio ativo no momento.")
    else:
        for d in desafios:
            with st.container(border=True):
                st.write(f"### {d['nome']}")
                st.markdown('<span style="font-size:12px; color:#1D9E75; background:#085041; padding:2px 10px; border-radius:999px;">em andamento</span>', unsafe_allow_html=True)
                # O botão agora usa o ID no key para não dar conflito de nomes repetidos
                if st.button(f"Acessar desafio", key=f"btn_acessar_{d['id']}"):
                    st.session_state.desafio = d['nome']
                    ir('votacao')

    st.divider()
    if st.button("Ver votos cadastrados"):
        ir('visualizar')