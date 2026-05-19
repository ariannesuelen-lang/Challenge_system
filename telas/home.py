import streamlit as st


def tela_home():

    usuario = st.session_state.usuario_logado

    st.title(
        f"Bem-vindo(a), {usuario['nome']}"
    )

    st.divider()

    st.subheader(
        "Desafios disponíveis"
    )

    st.warning(
        "Sistema em construção"
    )

    st.divider()

    st.subheader(
        "Desafios disponíveis para votação"
    )

    st.info(
        "Nenhum desafio disponível para voto"
    )

    st.divider()

    st.subheader(
        "Mini-provas"
    )

    st.warning(
        "Sistema em construção"
    )


    st.divider()

    st.subheader(
        "Quiz ao Vivo"
    )

    st.warning(
        "Sistema em construção"
    )

    st.divider()

    st.subheader(
        "Batalha de Equipes"
    )

    st.warning(
        "Sistema em construção"
    )
