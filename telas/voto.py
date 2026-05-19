import streamlit as st
import pandas as pd

from services.votacao_service import (
    buscar_voto_usuario,
    registrar_voto,
    atualizar_voto,
    deletar_voto,
    listar_votos_desafio
)


def tela_voto():

    desafio = st.session_state.desafio_voto

    usuario = st.session_state.usuario_logado

    st.title(
        desafio["titulo"]
    )

    st.write(
        f"Prazo: {desafio['prazo']}"
    )

    if st.button("Voltar"):

        st.session_state.pagina = "votacao"

        st.rerun()

    st.divider()

    voto_existente = buscar_voto_usuario(
        usuario["email"],
        desafio["titulo"]
    )

    opcoes = [
        "Bom",
        "Regular",
        "Ruim"
    ]

    editar = False

    if voto_existente:

        st.success(
            f"Seu voto atual: {voto_existente['voto']}"
        )

        if st.button("Editar voto"):

            st.session_state.editando_voto = True

            st.rerun()

        editar = st.session_state.get(
            "editando_voto",
            False
        )

    else:

        editar = True

    if editar:

        voto = st.radio(
            "Escolha seu voto",
            opcoes
        )

        if voto_existente:

            col1, col2 = st.columns(2)

            with col1:

                if st.button("Salvar edição"):

                    atualizar_voto(
                        voto_existente["id"],
                        voto
                    )

                    st.session_state.editando_voto = False

                    st.success(
                        "Voto atualizado"
                    )

                    st.rerun()

            with col2:

                if st.button("Excluir voto"):

                    deletar_voto(
                        voto_existente["id"]
                    )

                    st.session_state.editando_voto = False

                    st.success(
                        "Voto excluído"
                    )

                    st.rerun()

        else:

            if st.button("Enviar voto"):

                registrar_voto(
                    usuario["email"],
                    desafio["titulo"],
                    voto
                )

                st.success(
                    "Voto registrado"
                )

                st.rerun()

    st.divider()

    if st.button("Visualizar resultados"):

        st.session_state.mostrar_resultado = True

    if st.session_state.get(
        "mostrar_resultado",
        False
    ):

        votos = listar_votos_desafio(
            desafio["titulo"]
        )

        if votos:

            df = pd.DataFrame(votos)

            contagem = df["voto"].value_counts()

            contagem = contagem.reindex(
                ["Bom", "Regular", "Ruim"],
                fill_value=0
            )

            st.subheader("Resultado")

            st.bar_chart(contagem)

            st.write(
                f"Total de votos: {len(df)}"
            )

            # PROFESSOR E ADMIN
            if usuario["tipo_usuario"] in [
                "professor",
                "admin"
            ]:

                st.divider()

                st.subheader(
                    "Lista de votos"
                )

                for voto_item in votos:

                    with st.container(border=True):

                        st.write(
                            f"Aluno: {voto_item['usuario']}"
                        )

                        novo_voto = st.selectbox(
                            "Nota",
                            opcoes,
                            index=opcoes.index(
                                voto_item["voto"]
                            ),
                            key=f"select_{voto_item['id']}"
                        )

                        col1, col2 = st.columns(2)

                        with col1:

                            if st.button(
                                "Salvar",
                                key=f"salvar_{voto_item['id']}"
                            ):

                                atualizar_voto(
                                    voto_item["id"],
                                    novo_voto
                                )

                                st.success(
                                    "Voto atualizado"
                                )

                                st.rerun()

                        with col2:

                            if st.button(
                                "Excluir",
                                key=f"delete_{voto_item['id']}"
                            ):

                                deletar_voto(
                                    voto_item["id"]
                                )

                                st.success(
                                    "Voto excluído"
                                )

                                st.rerun()

        else:

            st.warning(
                "Nenhum voto encontrado"
            )
