import streamlit as st
from datetime import date
from services.batalha_de_equipes_service import (
    listar_batalhas, criar_batalha, finalizar_batalha
)


def tela_batalha_gerenciar():

    usuario = st.session_state.usuario_logado
    tipo    = usuario.get("tipo_usuario", "aluno")
    user_id = usuario.get("id")

    if tipo not in ("professor", "admin"):
        st.error("Acesso restrito a professores.")
        return

    st.title("Gerenciar Batalhas")

    if st.button("Voltar"):
        st.session_state.pagina = "batalha_de_equipes"
        st.rerun()

    st.divider()

    st.subheader("Nova Batalha")

    with st.container(border=True):

        titulo    = st.text_input("Titulo da batalha")
        descricao = st.text_area("Descricao / objetivo")
        prazo     = st.date_input("Prazo", value=None, min_value=date.today())

        if st.button("Criar batalha"):
            if not titulo.strip():
                st.warning("O titulo e obrigatorio.")
            else:
                if criar_batalha(titulo, descricao, user_id, prazo):
                    st.success("Batalha criada com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao criar batalha.")

    st.divider()
    st.subheader("Batalhas cadastradas")

    batalhas = listar_batalhas()

    if not batalhas:
        st.info("Nenhuma batalha cadastrada ainda.")
        return

    for b in batalhas:

        bid        = b.get("id")
        finalizada = b.get("finalizada", False)
        status_txt = "Finalizada" if finalizada else "Em aberto"

        with st.container(border=True):

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**{b.get('titulo')}**")
                st.caption(
                    f"Status: {status_txt} | "
                    f"Prazo: {b.get('prazo') or 'sem prazo'}"
                )
                if b.get("descricao"):
                    st.write(b["descricao"])

            with col2:
                if not finalizada:
                    if st.button("Finalizar", key=f"fin_{bid}"):
                        finalizar_batalha(bid)
                        st.success("Batalha finalizada.")
                        st.rerun()
                else:
                    st.info("Encerrada")
