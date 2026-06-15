# utils/session.py
import streamlit as st

def iniciar_session():
    """Inicializa as variáveis de controle global do Streamlit"""
    if "usuario_logado" not in st.session_state:
        st.session_state.usuario_logado = None

    if "pagina" not in st.session_state:
        st.session_state.pagina = "login"

    if "alto_contraste" not in st.session_state:
        st.session_state.alto_contraste = False