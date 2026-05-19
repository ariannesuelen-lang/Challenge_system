import streamlit as st
import pandas as pd

from services.votacao_service import (
    listar_desafios_votacao,
    registrar_voto,
    listar_votos_desafio,
    buscar_voto_usuario,
    atualizar_voto
)

def tela_votacao():

    st.title("Votação")

    usuario = st.session_state.usuario_logado

    desafios = listar_desafios_votacao()

    if "desafio_selecionado" not in st.session_state:

        st.session_state.desafio_selecionado = None

    # LISTA DE DESAFIOS
    if st.session_state.desafio_selecionado is None:

        st.subheader(
            "Desafios disponíveis"
        )

        for desafio in desafios:

            with st.container(border=True):

                st.write(
                    desafio["titulo"]
                )

                if st.button(
                    "Abrir",
                    key=f"abrir_{desafio['id']}"
                ):

                    st.session_state.desafio_selecionado = desafio

                    st.rerun()

    # TELA DO DESAFIO
    else:

        desafio = st.session_state.desafio_selecionado

        if st.button("Voltar"):

            st.session_state.desafio_selecionado = None

            st.rerun()

        st.subheader(
            desafio["titulo"]
        )

        st.write(
            desafio["descricao"]
        )

        st.write(
            f"Prazo: {desafio['prazo']}"
        )

        voto_usuario = buscar_voto_usuario(
            usuario["email"],
            desafio["titulo"]
        )

        st.divider()

        # USUÁRIO AINDA NÃO VOTOU
        if not voto_usuario:

            voto = st.radio(
                "Escolha seu voto",
                ["Bom", "Regular", "Ruim"]
            )

            if st.button(
                "Enviar voto"
            ):

                registrar_voto(
                    usuario["email"],
                    desafio["titulo"],
                    voto
                )

                st.success(
                    "Voto registrado"
                )

                st.rerun()

        # USUÁRIO JÁ VOTOU
        else:

            st.success(
                f"Seu voto atual: {voto_usuario['voto']}"
            )

            novo_voto = st.radio(
                "Editar voto",
                ["Bom", "Regular", "Ruim"],
                index=[
                    "Bom",
                    "Regular",
                    "Ruim"
                ].index(voto_usuario["voto"])
            )

            if st.button(
                "Salvar alteração"
            ):

                atualizar_voto(
                    voto_usuario["id"],
                    novo_voto
                )

                st.success(
                    "Voto atualizado"
                )

                st.rerun()

        st.divider()

        votos = listar_votos_desafio(
            desafio["titulo"]
        )

        if votos:

            df = pd.DataFrame(votos)

            contagem = (
                df["voto"]
                .value_counts()
            )

            contagem = contagem.reindex(
                ["Bom", "Regular", "Ruim"],
                fill_value=0
            )

            st.subheader(
                "Resultado"
            )

st.bar_chart(contagem)

            st.write(
                contagem
            )

        else:

            st.info(
                "Nenhum voto registrado"
            )
