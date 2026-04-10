import streamlit as st
from frontend.api import get, post, delete
import requests

BASE_URL = "http://localhost:8000"


def admin_id():
    return st.session_state.usuario["id"]


def render():
    st.subheader("⚙️ Painel Administrativo")

    aba = st.tabs(["👥 Usuários", "📋 Desafios", "💬 Respostas", "🏫 Cursos", "📗 Disciplinas"])

    # ── Usuários ──
    with aba[0]:
        st.markdown("### Gerenciar Usuários")
        usuarios = get(f"/admin/usuarios", params={"admin_id": admin_id()})
        for u in usuarios:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**{u['nome']}** — {u['email']}")
            with col2:
                novo_tipo = st.selectbox(
                    "Tipo",
                    ["aluno", "professor"],
                    index=0 if u["tipo_usuario"] == "aluno" else 1,
                    key=f"tipo_{u['id']}"
                )
                if st.button("Salvar", key=f"salvar_{u['id']}"):
                    res = requests.put(
                        f"{BASE_URL}/admin/usuarios/{u['id']}/tipo",
                        json={"novo_tipo": novo_tipo},
                        params={"admin_id": admin_id()}
                    )
                    if res.status_code == 200:
                        st.success("Tipo atualizado!")
                        st.rerun()
            with col3:
                if st.button("🗑️", key=f"del_user_{u['id']}"):
                    res = delete(f"/admin/usuarios/{u['id']}", params={"admin_id": admin_id()})
                    if res and res.status_code == 200:
                        st.warning("Usuário deletado.")
                        st.rerun()

    # ── Desafios ──
    with aba[1]:
        st.markdown("### Todos os Desafios")
        desafios = get("/desafios")
        for d in desafios:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"**{d['titulo']}** — {d.get('criador_nome', '')}")
            with col2:
                if st.button("🗑️", key=f"del_des_{d['id']}"):
                    res = delete(f"/admin/desafios/{d['id']}", params={"admin_id": admin_id()})
                    if res and res.status_code == 200:
                        st.warning("Desafio deletado.")
                        st.rerun()

    # ── Respostas ──
    with aba[2]:
        st.markdown("### Respostas por Desafio")
        desafios = get("/desafios")
        opts = {f"{d['titulo']}": d["id"] for d in desafios}
        if opts:
            sel = st.selectbox("Selecione o desafio", list(opts.keys()))
            respostas = get(f"/desafios/{opts[sel]}/respostas")
            for r in respostas:
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.write(f"👤 **{r['usuario_nome']}:** {r['conteudo']}")
                with col2:
                    if st.button("🗑️", key=f"del_res_{r['id']}"):
                        res = delete(f"/admin/respostas/{r['id']}", params={"admin_id": admin_id()})
                        if res and res.status_code == 200:
                            st.warning("Resposta deletada.")
                            st.rerun()

    # ── Cursos ──
    with aba[3]:
        st.markdown("### Gerenciar Cursos")
        cursos = get("/cursos")
        for c in cursos:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"📘 **{c['nome']}**")
            with col2:
                if st.button("🗑️", key=f"del_cur_{c['id']}"):
                    res = delete(f"/admin/cursos/{c['id']}", params={"admin_id": admin_id()})
                    if res and res.status_code == 200:
                        st.warning("Curso deletado.")
                        st.rerun()

        st.markdown("---")
        nome_curso = st.text_input("Nome do novo curso")
        if st.button("Criar Curso"):
            res = post("/cursos", {"nome": nome_curso})
            if res and res.status_code == 200:
                st.success("Curso criado!")
                st.rerun()

    # ── Disciplinas ──
    with aba[4]:
        st.markdown("### Gerenciar Disciplinas")
        disciplinas = get("/disciplinas")
        for d in disciplinas:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"📗 **{d['nome']}** — {d['curso_nome']}")
            with col2:
                if st.button("🗑️", key=f"del_disc_{d['id']}"):
                    res = delete(f"/admin/disciplinas/{d['id']}", params={"admin_id": admin_id()})
                    if res and res.status_code == 200:
                        st.warning("Disciplina deletada.")
                        st.rerun()

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