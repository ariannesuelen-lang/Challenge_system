import streamlit as st


def tela_mini_provas_professor():

    st.title(
        "Painel do Professor"
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

    for i in range(3):

        with st.container(border=True):

            st.write(
                f"Mini prova {i+1}"
            )

            st.write(
                "Disciplina: Matemática"
            )

            st.write(
                "5 perguntas"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.button(
                    f"Editar {i}"
                )

            with col2:

                st.button(
                    f"Visualizar {i}"
                )
