import streamlit as st
from frontend.api import get, put, delete


def user_id():
    return st.session_state.usuario["id"]


def render():
    st.subheader("✏️ Gerenciar Desafios")

    desafios = get("/desafios")
    meus = [d for d in desafios if d["criador_id"] == user_id()]

    if not meus:
        st.info("Você ainda não criou nenhum desafio.")
        return

    opcoes = {f"ID {d['id']} — {d['titulo']}": d for d in meus}
    sel = st.selectbox("Selecione o desafio", list(opcoes.keys()))
    desafio = opcoes[sel]

    disciplinas = get("/disciplinas")
    opts_disc = {"(Nenhuma)": None}
    opts_disc.update({d["nome"]: d["id"] for d in disciplinas})

    titulo = st.text_input("Título", value=desafio["titulo"])
    descricao = st.text_area("Descrição", value=desafio.get("descricao", ""))
    disc_atual = next((k for k, v in opts_disc.items() if v == desafio.get("disciplina_id")), "(Nenhuma)")
    disc_sel = st.selectbox("Disciplina", list(opts_disc.keys()), index=list(opts_disc.keys()).index(disc_atual))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Atualizar"):
            res = put(f"/desafios/{desafio['id']}", {
                "titulo": titulo,
                "descricao": descricao,
                "disciplina_id": opts_disc[disc_sel],
                "data_limite": desafio.get("data_limite")
            }, params={"usuario_id": user_id()})
            if res and res.status_code == 200:
                st.success("Desafio atualizado!")
                st.rerun()
            elif res:
                st.error(res.json().get("detail"))
    with col2:
        if st.button("🗑️ Deletar"):
            res = delete(f"/desafios/{desafio['id']}", params={"usuario_id": user_id()})
            if res and res.status_code == 200:
                st.warning("Desafio deletado.")
                st.rerun()
            elif res:
                st.error(res.json().get("detail"))