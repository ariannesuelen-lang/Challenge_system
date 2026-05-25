import streamlit as st


def tela_notificacoes_mini_provas():

    st.title("Notificações")

    notificacoes = [
        "Sua solicitação foi aprovada",
        "Nova mini prova disponível",
        "Resultado liberado"
    ]

    for notificacao in notificacoes:

        st.info(notificacao)

    st.divider()

    if st.button("Voltar"):

        st.switch_page(
            "telas/mini_provas/mini_provas_professor.py"
        )
