import streamlit as st
from frontend.api import get, post


def is_professor():
    return st.session_state.usuario and st.session_state.usuario["tipo_usuario"] == "professor"


def render():
    st.subheader("🏫 Cursos e Disciplinas")

    aba = st.tabs(["Cursos", "Disciplinas"])

    with aba[0]:
        cursos = get("/cursos")
        if cursos:
            for c in cursos:
                st.write(f"📘 **{c['nome']}** (ID: {c['id']})")
        else:
            st.info("Nenhum curso cadastrado.")

        if is_professor():
            st.markdown("---")
            nome_curso = st.text_input("Nome do novo curso")
            if st.button("Criar Curso"):
                res = post("/cursos", {"nome": nome_curso})
                if res and res.status_code == 200:
                    st.success("Curso criado!")
                    st.rerun()

    with aba[1]:
        disciplinas = get("/disciplinas")
        if disciplinas:
            for d in disciplinas:
                st.write(f"📗 **{d['nome']}** — Curso: {d['curso_nome']} (ID: {d['id']})")
        else:
            st.info("Nenhuma disciplina cadastrada.")

        if is_professor():
            st.markdown("---")
            cursos = get("/cursos")
            opts_curso = {c["nome"]: c["id"] for c in cursos}
            nome_disc = st.text_input("Nome da nova disciplina")
            if opts_curso:
                curso_sel = st.selectbox("Curso", list(opts_curso.keys()))
                if st.button("Criar Disciplina"):
                    res = post("/disciplinas", {"nome": nome_disc, "curso_id": opts_curso[curso_sel]})
                    if res and res.status_code == 200:
                        st.success("Disciplina criada!")
                        st.rerun()
            else:
                st.warning("Cadastre um curso antes de criar disciplinas.")