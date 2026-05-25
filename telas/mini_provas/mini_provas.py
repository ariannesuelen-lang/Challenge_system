import streamlit as st


def tela_mini_provas():

    if st.session_state.alto_contraste:

        st.markdown(
            """
            <style>

            .stApp {
                background-color: black;
                color: white;
            }

            </style>
            """,
            unsafe_allow_html=True
        )

    st.title("Mini Provas")

    col1, col2, col3 = st.columns(3)

    with col1:

        if st.button(
            "Minha Pontuação"
        ):

            st.session_state.pagina = (
                "pontuacao_mini_provas"
            )

            st.rerun()

    with col2:

        if st.button(
            "Desempenho"
        ):

            st.session_state.pagina = (
                "desempenho_mini_provas"
            )

            st.rerun()

    with col3:

        with st.popover(
            "Acessibilidade"
        ):

            alto = st.checkbox(
                "Alto contraste",
                value=st.session_state.alto_contraste
            )

            st.session_state.alto_contraste = alto

            leitura = st.checkbox(
                "Leitura por questão"
            )

            st.divider()

            st.subheader(
                "Solicitar tempo extra"
            )

            prova = st.selectbox(
                "Mini prova",
                [
                    "Mini prova 1",
                    "Mini prova 2"
                ]
            )

            justificativa = st.text_area(
                "Justificativa"
            )

            if st.button(
                "Enviar solicitação"
            ):

                st.success(
                    "Solicitação enviada"
                )

    st.divider()

    pesquisa = st.text_input(
        "Pesquisar mini prova"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "Mini Provas Disponíveis"
        )

    with col2:

        if st.button(
            "Resultados"
        ):

            st.session_state.pagina = (
                "resultados_mini_provas"
            )

            st.rerun()

    for i in range(3):

        with st.container(border=True):

            st.write(
                f"Mini prova {i+1}"
            )

            st.write(
                "Disciplina: Grafos aplicados a programação"
            )

            st.write(
                "5 perguntas"
            )

            st.write(
                "Valor: 1 ponto"
            )

            if st.button(
                f"Fazer prova {i}"
            ):

                st.session_state.pagina = (
                    "realizar_mini_prova"
                )

                st.rerun()
