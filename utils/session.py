import streamlit as st


def iniciar_session():

    if "usuario_logado" not in st.session_state:
        st.session_state.usuario_logado = None

    if "pagina" not in st.session_state:
        st.session_state.pagina = "login"
