import streamlit as st

from services.mini_prova_service import (
    criar_mini_prova
)


def tela_cadastro_mini_provas():

    st.title("Cadastro de Mini Provas")

    titulo = st.text_input("Título")

    disciplina = st.text_input("Disciplina")

    assunto = st.text_input("Assunto")

    quantidade_total = st.number_input(
        "Quantidade total de perguntas",
        min_value=1,
        step=1
    )

    quantidade_faceis = st.number_input(
        "Perguntas fáceis",
        min_value=0,
        step=1
    )

    quantidade_medias = st.number_input(
        "Perguntas médias",
        min_value=0,
        step=1
    )

    quantidade_dificeis = st.number_input(
        "Perguntas difíceis",
        min_value=0,
        step=1
    )

    tempo_minutos = st.number_input(
        "Tempo da prova (minutos)",
        min_value=1,
        step=1
    )

    pontos = st.number_input(
        "Pontuação da mini prova",
        min_value=0.1,
        step=0.1
    )

    if st.button("Criar Mini Prova"):

        soma = (
            quantidade_faceis +
            quantidade_medias +
            quantidade_dificeis
        )

        if soma != quantidade_total:

            st.error(
                "A soma das dificuldades deve ser igual ao total de perguntas"
            )

            return

        dados = {

            "titulo": titulo,

            "descricao": assunto,

            "qtde_questoes": quantidade_total,

            "duracao_minutos": tempo_minutos,

            "max_tentativas": 1,

            "randomizar_questoes": True,

            "randomizar_alternativas": True
        }

        criar_mini_prova(dados)

        st.success(
            "Mini prova criada com sucesso"
        )

    st.divider()

    if st.button("Voltar"):

        st.session_state.pagina = "mini_provas"

        st.rerun()
