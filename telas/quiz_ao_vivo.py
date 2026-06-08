import streamlit as st
from services.votacao_service import listar_desafios_votacao
from utils.estilo import aplicar_estilo, cabecalho


def tela_votacao():

    aplicar_estilo()
    cabecalho("Votação", "Vote nos desafios disponíveis")

    pesquisa = st.text_input("Pesquisar desafio")
    desafios = listar_desafios_votacao()

    if pesquisa:
        desafios = [
            d for d in desafios
            if pesquisa.lower() in d["titulo"].lower()
        ]

    if not desafios:
        st.warning("Nenhum desafio encontrado.")
        return

    for desafio in desafios:
        st.markdown(f"""
        <div style="
            background:#f0f9ff;
            border-left:4px solid #00b4d8;
            border-radius:8px;
            padding:14px 18px;
            margin-bottom:10px;
        ">
            <strong style="color:#0d1b2a; font-size:15px;">{desafio['titulo']}</strong><br>
            <span style="color:#00b4d8; font-size:12px;">Prazo: {desafio['data_limite']}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Abrir", key=f"abrir_{desafio['id']}", use_container_width=False):
            st.session_state.desafio_voto = desafio
            st.session_state.pagina = "voto"
            st.rerun()
