import streamlit as st

from services.mini_prova_service import (
    listar_mini_provas
)


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
            "Ver Perguntas"
        ):

            st.session_state.pagina = (
                "lista_perguntas"
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

    else:

        for prova in mini_provas:

            with st.container(border=True):

                st.write(
                    prova["titulo"]
                )

                st.write(
                    prova["descricao"]
                )

                st.write(
                    f"{prova['qtde_questoes']} questões"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "Editar",
                        key=f"editar_{prova['id']}"
                    ):

                        st.session_state.id_mini_prova = (
                            prova["id"]
                        )

                        st.session_state.pagina = (
                            "editar_mini_prova"
                        )

                        st.rerun()

                with col2:

                    if st.button(
                        "Visualizar",
                        key=f"visualizar_{prova['id']}"
                    ):

                        st.session_state.id_mini_prova = (
                            prova["id"]
                        )

                        st.session_state.pagina = (
                            "visualizar_mini_prova"
                        )

                        st.rerun()
