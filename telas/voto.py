import streamlit as st
import pandas as pd
from services.votacao_service import (
    buscar_voto_usuario,
    registrar_voto,
    atualizar_voto,
    deletar_voto,
    listar_votos_desafio
)
from utils.estilo import aplicar_estilo, cabecalho


def tela_voto():

    aplicar_estilo()

    desafio = st.session_state.desafio_voto
    usuario = st.session_state.usuario_logado

    cabecalho(desafio["titulo"], f"Prazo: {desafio['data_limite']}")

    if st.button("Voltar para Votação"):
        st.session_state.pagina = "votacao"
        st.rerun()

    st.divider()

    voto_existente = buscar_voto_usuario(usuario["email"], desafio["titulo"])
    opcoes = ["Bom", "Regular", "Ruim"]

    if voto_existente:
        st.markdown(f"""
        <div style="
            background:#f0f9ff;
            border-left:4px solid #00b4d8;
            border-radius:8px;
            padding:14px 18px;
            margin-bottom:12px;
        ">
            <strong style="color:#0d1b2a;">Seu voto atual: {voto_existente['voto']}</strong>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Editar voto", use_container_width=True):
                st.session_state.editando_voto = True
        with col2:
            if st.button("Deletar voto", use_container_width=True):
                deletar_voto(usuario["email"], desafio["titulo"])
                st.success("Voto deletado.")
                st.rerun()

        if st.session_state.get("editando_voto"):
            with st.container(border=True):
                novo_voto = st.selectbox("Novo voto", opcoes)
                if st.button("Salvar", use_container_width=True):
                    atualizar_voto(usuario["email"], desafio["titulo"], novo_voto)
                    st.success("Voto atualizado!")
                    st.session_state.editando_voto = False
                    st.rerun()
    else:
        with st.container(border=True):
            st.markdown("### Registrar voto")
            voto = st.selectbox("Sua avaliação", opcoes)
            if st.button("Votar", use_container_width=True):
                registrar_voto(usuario["email"], desafio["titulo"], voto)
                st.success("Voto registrado!")
                st.rerun()

    st.divider()
    st.markdown("### Votos registrados")
    votos = listar_votos_desafio(desafio["titulo"])
    if votos:
        df = pd.DataFrame(votos)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum voto registrado ainda.")
