import streamlit as st
from frontend.pages import login, desafios, criar_desafio, gerenciar, cursos, admin, detalhe_curso

if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "pagina" not in st.session_state:
    st.session_state.pagina = "desafios"
if "curso_selecionado" not in st.session_state:
    st.session_state.curso_selecionado = None
if "disciplina_selecionada" not in st.session_state:
    st.session_state.disciplina_selecionada = None


def sistema():
    usuario = st.session_state.usuario
    tipo = usuario["tipo_usuario"]

    st.sidebar.title(f"👤 {usuario['nome']}")
    st.sidebar.caption(tipo.capitalize())

    if st.sidebar.button("Sair"):
        for key in ["logado", "usuario", "pagina", "curso_selecionado", "disciplina_selecionada"]:
            st.session_state[key] = None
        st.session_state.logado = False
        st.rerun()

    st.sidebar.markdown("---")

    # Navegação principal por tipo
    if st.sidebar.button("📋 Desafios"):
        st.session_state.pagina = "desafios"
        st.rerun()

    if tipo in ("professor", "admin"):
        if st.sidebar.button("➕ Criar Desafio"):
            st.session_state.pagina = "criar_desafio"
            st.rerun()
        if st.sidebar.button("✏️ Gerenciar Desafios"):
            st.session_state.pagina = "gerenciar"
            st.rerun()

    if tipo == "admin":
        if st.sidebar.button("⚙️ Painel Admin"):
            st.session_state.pagina = "admin"
            st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏫 Cursos")

    # Cursos e disciplinas clicáveis
    from frontend.api import get
    cursos_lista = get("/cursos")
    for c in cursos_lista:
        if st.sidebar.button(f"📘 {c['nome']}", key=f"curso_{c['id']}"):
            st.session_state.curso_selecionado = c
            st.session_state.disciplina_selecionada = None
            st.session_state.pagina = "detalhe_curso"
            st.rerun()

        disciplinas_lista = get("/disciplinas", params={"curso_id": c["id"]})
        for d in disciplinas_lista:
            if st.sidebar.button(f"  📗 {d['nome']}", key=f"disc_{d['id']}"):
                st.session_state.disciplina_selecionada = d
                st.session_state.curso_selecionado = c
                st.session_state.pagina = "detalhe_curso"
                st.rerun()

    # Renderiza página ativa
    pagina = st.session_state.pagina

    if pagina == "desafios":
        desafios.render()
    elif pagina == "criar_desafio":
        criar_desafio.render()
    elif pagina == "gerenciar":
        gerenciar.render()
    elif pagina == "admin":
        admin.render()
    elif pagina == "detalhe_curso":
        detalhe_curso.render()


if not st.session_state.logado:
    login.render()
else:
    sistema()