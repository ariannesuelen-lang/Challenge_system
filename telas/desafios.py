import streamlit as st
from datetime import date

from services.desafio_service import (
    criar_desafio,
    listar_desafios,
    deletar_desafio
)
from utils.estilo import aplicar_estilo, cabecalho


def tela_desafios():

    aplicar_estilo()

    usuario = st.session_state.usuario_logado

    if usuario["tipo_usuario"] != "professor":
        cabecalho("Desafios", "Desafios disponíveis")
        desafios = listar_desafios()
        if not desafios:
            st.info("Nenhum desafio disponível no momento.")
            return
        for d in desafios:
            st.markdown(f"""
            <div style="
                background:#f0f9ff;
                border-left:4px solid #00b4d8;
                border-radius:8px;
                padding:12px 16px;
                margin-bottom:8px;
            ">
                <strong style="color:#0d1b2a;">{d['titulo']}</strong><br>
                <span style="color:#555; font-size:13px;">{d.get('descricao','')}</span><br>
                <span style="color:#00b4d8; font-size:12px;">
                    Nível: {d.get('nivel','-')} &nbsp;|&nbsp;
                    Prazo: {d.get('data_limite','-')}
                </span>
            </div>
            """, unsafe_allow_html=True)
        return

    cabecalho("Desafios", "Crie e gerencie os desafios")

    aba = st.tabs(["Criar", "Listar", "Deletar"])

    # ---- CRIAR ----
    with aba[0]:
        st.markdown("### Novo desafio")
        with st.container(border=True):
            criador_id    = usuario["id"]
            titulo        = st.text_input("Título")
            descricao     = st.text_area("Descrição")
            nivel         = st.selectbox("Nível", ["Fácil", "Médio", "Difícil"])
            disciplina_id = st.number_input("ID da Disciplina", min_value=1, step=1)
            data_limite   = st.date_input("Data Limite", min_value=date.today())

            if st.button("Criar Desafio", use_container_width=True):
                resultado = criar_desafio(
                    titulo, descricao, nivel,
                    criador_id, disciplina_id, data_limite,
                )
                if resultado["sucesso"]:
                    st.success("Desafio criado com sucesso!")
                else:
                    st.error(resultado["mensagem"])

    # ---- LISTAR ----
    with aba[1]:
        st.markdown("### Lista de desafios")
        desafios = listar_desafios()
        if not desafios:
            st.info("Nenhum desafio cadastrado.")
        for d in desafios:
            st.markdown(f"""
            <div style="
                background:#f0f9ff;
                border-left:4px solid #00b4d8;
                border-radius:8px;
                padding:12px 16px;
                margin-bottom:8px;
            ">
                <strong style="color:#0d1b2a;">#{d['id']} — {d['titulo']}</strong><br>
                <span style="color:#555; font-size:13px;">{d.get('descricao','')}</span>
            </div>
            """, unsafe_allow_html=True)

    # ---- DELETAR ----
    with aba[2]:
        st.markdown("### Deletar desafio")
        desafios = listar_desafios()
        if not desafios:
            st.info("Nenhum desafio para deletar.")
        else:
            ids          = [d["id"] for d in desafios]
            id_escolhido = st.selectbox("Selecione o desafio", ids)
            if st.button("Deletar", use_container_width=True):
                deletar_desafio(id_escolhido)
                st.warning("Desafio deletado!")
                st.rerun()
