import streamlit as st
from frontend.api import get, post
from frontend.pages import criar_desafio


def user_id():
    return st.session_state.usuario["id"]


def tipo():
    return st.session_state.usuario["tipo_usuario"]


def render():
    curso = st.session_state.curso_selecionado
    disciplina = st.session_state.disciplina_selecionada

    # Exibe detalhe de uma disciplina específica
    if disciplina:
        st.subheader(f"📗 {disciplina['nome']}")
        st.caption(f"Curso: {curso['nome']}")
        st.markdown("---")

        st.markdown("### 📋 Desafios desta disciplina")
        desafios = get("/desafios", params={"disciplina_id": disciplina["id"]})
        if desafios:
            for d in desafios:
                with st.expander(f"📌 {d['titulo']}"):
                    st.write(f"**Criado por:** {d['criador_nome']}")
                    if d.get("descricao"):
                        st.write(f"**Descrição:** {d['descricao']}")
                    if d.get("data_limite"):
                        st.write(f"**Prazo:** {d['data_limite'][:10]}")

                    st.markdown("**💬 Respostas:**")
                    respostas = get(f"/desafios/{d['id']}/respostas")
                    if respostas:
                        for r in respostas:
                            col1, col2 = st.columns([4, 1])
                            with col1:
                                st.write(f"👤 **{r['usuario_nome']}:** {r['conteudo']}")
                            with col2:
                                votos = r.get("total_votos", 0)
                                if st.button(f"👍 {votos}", key=f"voto_disc_{r['id']}"):
                                    res = post("/votos", {"resposta_id": r["id"], "usuario_id": user_id()})
                                    if res and res.status_code == 200:
                                        st.success("Voto registrado!")
                                        st.rerun()
                                    elif res:
                                        st.warning(res.json().get("detail"))
                    else:
                        st.info("Nenhuma resposta ainda.")

                    st.markdown("---")
                    with st.form(key=f"form_disc_{d['id']}"):
                        conteudo = st.text_area("Sua resposta", key=f"resp_disc_{d['id']}")
                        if st.form_submit_button("Enviar resposta"):
                            res = post("/respostas", {
                                "desafio_id": d["id"],
                                "usuario_id": user_id(),
                                "usuario_tipo": tipo(),
                                "conteudo": conteudo
                            })
                            if res and res.status_code == 200:
                                st.success("Resposta enviada!")
                                st.rerun()
        else:
            st.info("Nenhum desafio nesta disciplina ainda.")

    # Exibe detalhe do curso com todas as disciplinas
    else:
        st.subheader(f"📘 {curso['nome']}")
        st.markdown("---")

        disciplinas = get("/disciplinas", params={"curso_id": curso["id"]})
        if not disciplinas:
            st.info("Nenhuma disciplina cadastrada neste curso.")
            return

        for d in disciplinas:
            with st.expander(f"📗 {d['nome']}"):
                desafios = get("/desafios", params={"disciplina_id": d["id"]})
                if desafios:
                    for des in desafios:
                        st.write(f"📌 **{des['titulo']}** — {des['criador_nome']}")
                        if des.get("descricao"):
                            st.caption(des["descricao"])
                        if st.button(f"Ver desafio completo", key=f"ver_{des['id']}"):
                            st.session_state.disciplina_selecionada = d
                            st.rerun()
                else:
                    st.info("Nenhum desafio nesta disciplina.")