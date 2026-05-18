import streamlit as st
import pandas as pd

from services.votacao_service import (

    listar_desafios_votacao,
    salvar_voto,
    buscar_voto_usuario,
    listar_votos_desafio
)


def tela_votacao():

    st.title("Votação")

    usuario = (
        st.session_state.usuario_logado
    )

    desafios = (
        listar_desafios_votacao()
    )

    if not desafios:

        st.warning(
            "Nenhum desafio disponível para votação"
        )

        return

    for desafio in desafios:

        with st.container(border=True):

            st.subheader(
                desafio["titulo"]
            )

            st.write(
                desafio["descricao"]
            )

            voto_existente = (
                buscar_voto_usuario(
                    desafio["id"],
                    usuario["id"]
                )
            )

            valor_inicial = 0

            opcoes = [
                "Bom",
                "Regular",
                "Ruim"
            ]

            if voto_existente:

                valor_inicial = (
                    opcoes.index(
                        voto_existente["nota"]
                    )
                )

            nota = st.radio(

                "Escolha sua nota",

                opcoes,

                index=valor_inicial,

                key=f"radio_{desafio['id']}"
            )

            if st.button(

                "Salvar voto",

                key=f"voto_{desafio['id']}"
            ):

                salvar_voto(

                    desafio["id"],
                    usuario["id"],
                    nota
                )

                st.success(
                    "Voto salvo"
                )

                st.rerun()

            st.divider()

            votos = (
                listar_votos_desafio(
                    desafio["id"]
                )
            )

            if votos:

                df = pd.DataFrame(votos)

                contagem = (
                    df["nota"]
                    .value_counts()
                )

                contagem = contagem.reindex(

                    ["Bom", "Regular", "Ruim"],

                    fill_value=0
                )

                st.bar_chart(
                    contagem
                )
