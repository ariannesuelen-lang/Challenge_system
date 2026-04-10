import streamlit as st
from frontend.pages import login, desafios, criar_desafio, gerenciar, cursos

if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None

def sistema():
    usuario = st.session_state.usuario
    tipo = usuario["tipo_usuario"]

    st.sidebar.title(f"👤 {usuario['nome']}")
    st.sidebar.caption(f"{tipo.capitalize()}")

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.session_state.usuario = None
        st.rerun()

    st.sidebar.markdown("---")

    opcoes = ["📋 Desafios", "🏫 Cursos e Disciplinas"]
    if tipo == "professor":
        opcoes += ["➕ Criar Desafio", "✏️ Gerenciar Desafios"]

    menu = st.sidebar.radio("Navegação", opcoes)

    if menu == "📋 Desafios":
        desafios.render()
    elif menu == "🏫 Cursos e Disciplinas":
        cursos.render()
    elif menu == "➕ Criar Desafio":
        criar_desafio.render()
    elif menu == "✏️ Gerenciar Desafios":
        gerenciar.render()

if not st.session_state.logado:
    login.render()
else:
    sistema()