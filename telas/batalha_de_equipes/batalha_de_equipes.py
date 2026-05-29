import streamlit as st


def tela_batalha_de_equipes():

    usuario = st.session_state.usuario_logado
    tipo = usuario.get("tipo_usuario", "aluno")

    st.title("Batalha de Equipes")
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Times", use_container_width=True):
            st.session_state.pagina = "batalha_times"
            st.rerun()

    with col2:
        if st.button("Integrantes", use_container_width=True):
            st.session_state.pagina = "batalha_integrantes"
            st.rerun()

    with col3:
        if st.button("Regras", use_container_width=True):
            st.session_state.pagina = "batalha_regras"
            st.rerun()

    st.divider()

    if tipo == "professor":

        col4, col5 = st.columns(2)

        with col4:
            if st.button("Gerenciar Batalhas", use_container_width=True):
                st.session_state.pagina = "batalha_gerenciar"
                st.rerun()

        with col5:
            if st.button("Batalhas em Andamento", use_container_width=True):
                st.session_state.pagina = "batalha_rodada"
                st.rerun()

    else:

        col4, col5 = st.columns(2)

        with col4:
            if st.button("Batalhas Abertas", use_container_width=True):
                st.session_state.pagina = "batalha_rodada"
                st.rerun()

        with col5:
            if st.button("Minhas Respostas", use_container_width=True):
                st.session_state.pagina = "batalha_respostas"
                st.rerun()
