import streamlit as st
from services.mini_prova_service import listar_mini_provas


def tela_mini_provas_professor():

    st.title(
        "Painel de Mini Provas"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "Cadastrar Perguntas"
        ):

            st.session_state.pagina = (
                "cadastro_perguntas"
            )

            st.rerun()

    with col2:

        if st.button(
            "Cadastrar Mini Prova"
        ):

            st.session_state.pagina = (
                "cadastro_mini_provas"
            )

            st.rerun()

    with col3:

        if st.button(
            "Solicitações"
        ):

            st.session_state.pagina = (
                "solicitacoes_reabertura"
            )

            st.rerun()

    st.divider()

    st.subheader(
        "Mini Provas Criadas"
    )

    mini_provas = listar_mini_provas()

    if not mini_provas:

        st.info(
            "Nenhuma mini prova cadastrada"
        )

        return

    for prova in mini_provas:

        with st.container(border=True):

            st.write(
                prova["titulo"]
            )

            st.write(
                prova.get(
                    "descricao",
                    ""
                )
            )

            st.write(
                f"Duração: {prova['duracao_minutos']} minutos"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.button(
                    "Editar",
                    key=f"editar_{prova['id']}"
                )

            with col2:

                st.button(
                    "Visualizar",
                    key=f"visualizar_{prova['id']}"
                )
