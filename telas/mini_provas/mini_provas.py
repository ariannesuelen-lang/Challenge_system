import streamlit as st
from services.mini_prova_service import listar_mini_provas


def tela_mini_provas():

    usuario = st.session_state.usuario_logado

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

            mini_provas = listar_mini_provas()

            nomes = []

            for prova in mini_provas:

                nomes.append(
                    prova["titulo"]
                )

            if nomes:

                prova = st.selectbox(
                    "Mini prova",
                    nomes
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

    mini_provas = listar_mini_provas()

    if not mini_provas:

        st.info(
            "Nenhuma mini prova disponível"
        )

        return

    for prova in mini_provas:

        titulo = prova["titulo"]

        if pesquisa.lower() not in titulo.lower():

            continue

        with st.container(border=True):

            st.write(
                titulo
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

            if st.button(
                f"Fazer prova {prova['id']}"
            ):

                st.session_state.id_mini_prova = (
                    prova["id"]
                )

                st.session_state.pagina = (
                    "realizar_mini_prova"
                )

                st.rerun()
