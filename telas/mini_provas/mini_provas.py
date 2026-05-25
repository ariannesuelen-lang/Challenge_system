import streamlit as st
from services.mini_prova_service import listar_mini_provas


def tela_mini_provas():

    st.title("Mini Provas")

    st.button("Minha pontuação: 0")

    pesquisa = st.text_input("Pesquisar")

    provas = listar_mini_provas().data

    for prova in provas:

        if pesquisa.lower() in prova["titulo"].lower():

            st.subheader(prova["titulo"])

            st.write(prova["disciplina"])
            st.write(prova["assunto"])

            if st.button(
                f"Iniciar {prova['id']}"
            ):
                st.session_state["mini_prova"] = prova
