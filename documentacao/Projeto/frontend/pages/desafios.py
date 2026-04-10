import streamlit as st
from frontend.api import get, post


def user_id():
    return st.session_state.usuario["id"]


def render():
    st.subheader("📋 Desafios")

    disciplinas = get("/disciplinas")
    opcoes_disc = {"Todas": None}
    opcoes_disc.update({d["nome"]: d["id"] for d in disciplinas})
    filtro = st.selectbox("Filtrar por disciplina", list(opcoes_disc.keys()))
    disc_id = opcoes_disc[filtro]

    desafios = get("/desafios", params={"disciplina_id": disc_id} if disc_id else None)

    if not desafios:
        st.info("Nenhum desafio encontrado.")
        return

    for d in desafios:
        with st.expander(f"📌 {d['titulo']} — {d.get('disciplina_nome', 'Sem disciplina')}"):
            st.write(f"**Criado por:** {d['criador_nome']}")
            if d.get("descricao"):
                st.write(f"**Descrição:** {d['descricao']}")
            if d.get("data_limite"):
                st.write(f"**Prazo:** {d['data_limite'][:10]}")

            st.markdown("---")
            st.markdown("**💬 Respostas:**")

            respostas = get(f"/desafios/{d['id']}/respostas")
            if respostas:
                for r in respostas:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"👤 **{r['usuario_nome']}:** {r['conteudo']}")
                    with col2:
                        votos = r.get("total_votos", 0)
                        if st.button(f"👍 {votos}", key=f"voto_{r['id']}"):
                            res = post("/votos", {"resposta_id": r["id"], "usuario_id": user_id()})
                            if res and res.status_code == 200:
                                st.success("Voto registrado!")
                                st.rerun()
                            elif res:
                                st.warning(res.json().get("detail"))
            else:
                st.info("Nenhuma resposta ainda. Seja o primeiro!")

            st.markdown("---")
            with st.form(key=f"form_resp_{d['id']}"):
                conteudo = st.text_area("Sua resposta", key=f"resp_{d['id']}")
                if st.form_submit_button("Enviar resposta"):
                    res = post("/respostas", {
                        "desafio_id": d["id"],
                        "usuario_id": user_id(),
                        "conteudo": conteudo
                    })
                    if res and res.status_code == 200:
                        st.success("Resposta enviada!")
                        st.rerun()
                    elif res:
                        st.error(res.json().get("detail"))