import streamlit as st

def ir(pagina: str):
    st.session_state.pagina = pagina
    st.rerun()