import streamlit as st
from frontend.api import get, post


def user_id():
    return st.session_state.usuario["id"]


def render():
    st.subheader("➕ Criar Desafio")

    disciplinas = get("/disciplinas")
    opcoes = {"(Nenhuma)": None}
    opcoes.update({d["nome"]: d["id"] for d in disciplinas})

    titulo = st.text_input("Título do desafio")
    descricao = st.text_area("Descrição (opcional)")
    disc_sel = st.selectbox("Disciplina", list(opcoes.keys()))
    data_limite = st.date_input("Data limite (opcional)", value=None)

    if st.button("Criar Desafio"):
        res = post("/desafios", {
            "titulo": titulo,
            "descricao": descricao,
            "criador_id": user_id(),
            "disciplina_id": opcoes[disc_sel],
            "data_limite": str(data_limite) if data_limite else None
        })
        if res and res.status_code == 200:
            st.success("Desafio criado com sucesso!")
        elif res:
            st.error(res.json().get("detail"))