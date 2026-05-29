import streamlit as st
from services.batalha_de_equipes_service import (
    listar_times, criar_time, editar_time, deletar_time,
    aluno_tem_time, entrar_no_time
)


def tela_batalha_times():

    usuario = st.session_state.usuario_logado
    tipo    = usuario.get("tipo_usuario", "aluno")
    user_id = usuario.get("id")

    st.title("Times")

    if st.button("Voltar"):
        st.session_state.pagina = "batalha_de_equipes"
        st.rerun()

    st.divider()

    # --------------------------------------------------
    # PROFESSOR
    # --------------------------------------------------
    if tipo == "professor":

        st.subheader("Criar novo time")

        nome = st.text_input("Nome do time")

        if st.button("Criar"):
            if not nome or not nome.strip():
                st.warning("Nome nao pode ser vazio.")
            else:
                if criar_time(nome):
                    st.success(f"Time '{nome}' criado!")
                    st.rerun()
                else:
                    st.error("Erro ao criar time.")

        st.divider()
        st.subheader("Times cadastrados")

        times = listar_times()

        if not times:
            st.info("Nenhum time cadastrado ainda.")
            return

        for t in times:

            if not isinstance(t, dict):
                continue

            time_id    = t.get("id")
            nome_atual = t.get("nome", "")

            if not time_id or not nome_atual:
                continue

            with st.container(border=True):

                st.markdown(f"**{nome_atual}**")

                novo_nome = st.text_input(
                    "Editar nome",
                    value=nome_atual,
                    key=f"edit_{time_id}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("Salvar", key=f"salvar_{time_id}"):
                        if not novo_nome.strip():
                            st.warning("Nome nao pode ficar vazio.")
                        else:
                            editar_time(time_id, novo_nome)
                            st.success("Atualizado!")
                            st.rerun()

                with col2:
                    if st.button("Deletar", key=f"deletar_{time_id}"):
                        deletar_time(time_id)
                        st.success("Time removido.")
                        st.rerun()

    # --------------------------------------------------
    # ALUNO
    # --------------------------------------------------
    else:

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            st.error("Sessao invalida.")
            return

        if aluno_tem_time(user_id):
            st.success("Voce ja esta em um time.")
            st.info("Acesse Integrantes para ver seu time.")
            return

        st.subheader("Entrar em um time")

        times = listar_times()

        if not times:
            st.info("Nenhum time disponivel no momento.")
            return

        mapa = {
            t.get("nome"): t.get("id")
            for t in times
            if isinstance(t, dict) and t.get("nome") and t.get("id")
        }

        if not mapa:
            st.error("Dados invalidos de times.")
            return

        sel = st.selectbox("Selecione um time", list(mapa.keys()))

        if st.button("Entrar no time"):
            if entrar_no_time(mapa[sel], user_id):
                st.success(f"Voce entrou no time '{sel}'!")
                st.rerun()
            else:
                st.warning("Voce ja pertence a um time.")
