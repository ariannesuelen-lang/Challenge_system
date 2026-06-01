import streamlit as st

from services.mini_prova_service import (
    criar_pergunta
)


def tela_cadastro_perguntas():

    st.title("Cadastro de Perguntas")

    disciplina = st.text_input(
        "Disciplina"
    )

    assunto = st.text_input(
        "Assunto"
    )

    dificuldade = st.selectbox(
        "Dificuldade",
        [
            "facil",
            "media",
            "dificil"
        ]
    )

    pergunta = st.text_area(
        "Pergunta"
    )

    st.subheader("Alternativas")

    alternativa_a = st.text_input(
        "Alternativa A"
    )

    alternativa_b = st.text_input(
        "Alternativa B"
    )

    alternativa_c = st.text_input(
        "Alternativa C"
    )

    alternativa_d = st.text_input(
        "Alternativa D"
    )

    alternativa_e = st.text_input(
        "Alternativa E"
    )

    resposta_correta = st.selectbox(
        "Resposta correta",
        [
            "A",
            "B",
            "C",
            "D",
            "E"
        ]
    )

    if st.button(
        "Cadastrar pergunta"
    ):

        dados = {

            "enunciado": pergunta,

            "nivel": dificuldade
        }

        criar_pergunta(dados)

        st.success(
            "Pergunta cadastrada"
        )

    st.divider()

    if st.button("Voltar"):

        st.session_state.pagina = (
            "mini_provas"
        )

        st.rerun()
