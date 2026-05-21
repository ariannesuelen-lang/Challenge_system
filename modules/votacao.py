import streamlit as st
import pandas as pd
from conexao import listar_votos, inserir_voto
from modules.utils import ir

OPCOES = {
    "👍\n\nBom": "Bom",
    "😐\n\nRegular": "Regular",
    "👎\n\nRuim": "Ruim"
}

def render():
    if st.button("← Voltar", key="btn_voltar_votacao"):
        ir('lista')

    desafio = st.session_state.desafio
    st.write(f"### {desafio} - Votação")

    dados = listar_votos()
    ja_votou = False

    if dados.data:
        df = pd.DataFrame(dados.data)
        filtro = df[
            (df["usuario"] == st.session_state.id_usuario) &
            (df["desafio"] == desafio)
        ]
        if not filtro.empty:
            ja_votou = True

    if ja_votou:
        st.warning("⚠️ Você já registrou um voto para este desafio!")
    else:
        escolha = st.radio(
            "Escolha sua nota:",
            list(OPCOES.keys()),
            horizontal=True,
            label_visibility="collapsed",
            index=None
        )

        st.write("")

        if st.button("Enviar Voto", use_container_width=True, type="primary"):
            if escolha is None:
                st.warning("Por favor, selecione uma nota antes de enviar.")
            else:
                try:
                    inserir_voto(st.session_state.id_usuario, desafio, OPCOES[escolha])
                    st.success("Voto salvo com sucesso")
                    st.session_state.desafio = None
                    ir('lista')
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")