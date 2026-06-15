import streamlit as st

from services.mini_prova_service import (
    buscar_mini_prova
)


def tela_visualizar_mini_prova():

    st.title(
        "Visualizar Mini Prova"
    )

    id_mini_prova = (
        st.session_state.id_mini_prova
    )

    prova = buscar_mini_prova(
        id_mini_prova
    )

    if not prova:

        st.error(
            "Mini prova não encontrada"
        )

        return

    st.subheader(
        prova["titulo"]
    )

    st.write(
        prova["descricao"]
    )

    st.write(
        f"Quantidade de questões: {prova['qtde_questoes']}"
    )

    st.write(
        f"Duração: {prova['duracao_minutos']} minutos"
    )

    st.write(
        f"Status: {prova['status']}"
    )

    st.divider()

    if st.button("Voltar"):

        st.session_state.pagina = (
            "mini_provas"
        )

        st.rerun()
