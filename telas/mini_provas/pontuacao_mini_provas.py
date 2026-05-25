import streamlit as st


def tela_pontuacao_mini_provas():

    st.title("Minha Pontuação")

    st.metric("Pontuação Total", "4.2")

    st.metric("Posição", "3º")

    st.divider()

    st.subheader("Ranking")

    ranking = [
        "1º João - 5.0",
        "2º Maria - 4.5",
        "3º Você - 4.2"
    ]

    for jogador in ranking:

        st.write(jogador)

    st.divider()

    if st.button("Voltar"):

        st.switch_page(
            "telas/mini_provas/mini_provas.py"
        )
