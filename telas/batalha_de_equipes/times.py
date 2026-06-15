import streamlit as st
from services.batalha_de_equipes_service import (
    listar_times, criar_time, editar_time, deletar_time,
    aluno_tem_time, entrar_no_time
)
from utils.estilo import aplicar_estilo, cabecalho


def tela_batalha_times():

    aplicar_estilo()

    usuario = st.session_state.usuario_logado
    tipo    = usuario.get("tipo_usuario", "aluno")
    user_id = usuario.get("id")

    cabecalho("Times", "Gerencie ou entre em um time")

    if st.button("Voltar"):
        st.session_state.pagina = "batalha_de_equipes"
        st.rerun()

    st.divider()

    # --------------------------------------------------
    # PROFESSOR
    # --------------------------------------------------
    if tipo == "professor":

        st.markdown("### Criar novo time")

        with st.container(border=True):
            nome = st.text_input("Nome do time", placeholder="Ex: Time Alpha")
            if st.button("Criar time", use_container_width=True):
                if not nome or not nome.strip():
                    st.warning("Nome nao pode ser vazio.")
                else:
                    if criar_time(nome):
                        st.success(f"Time '{nome}' criado!")
                        st.rerun()
                    else:
                        st.error("Erro ao criar time.")

        st.divider()
        st.markdown("### Times cadastrados")

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
                col_titulo, col_acoes = st.columns([3, 1])

                with col_titulo:
                    st.markdown(f"""
                    <div style="
                        background:#f0f9ff;
                        border-left:4px solid #00b4d8;
                        border-radius:6px;
                        padding:8px 12px;
                    ">
                        <strong style="color:#0d1b2a; font-size:16px;">{nome_atual}</strong>
                    </div>
                    """, unsafe_allow_html=True)

                with st.expander("Editar / Deletar", expanded=False):
                    novo_nome = st.text_input(
                        "Novo nome",
                        value=nome_atual,
                        key=f"edit_{time_id}"
                    )
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Salvar", key=f"salvar_{time_id}", use_container_width=True):
                            if not novo_nome.strip():
                                st.warning("Nome nao pode ficar vazio.")
                            else:
                                editar_time(time_id, novo_nome)
                                st.success("Atualizado!")
                                st.rerun()
                    with col2:
                        if st.button("Deletar", key=f"deletar_{time_id}", use_container_width=True):
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
            st.markdown("""
            <div style="
                background:#e0f7fa;
                border-left:4px solid #00b4d8;
                border-radius:8px;
                padding:16px 20px;
            ">
                <strong style="color:#0d1b2a;">Voce ja esta em um time.</strong><br>
                <span style="color:#555;">Acesse a aba Integrantes para ver seu time.</span>
            </div>
            """, unsafe_allow_html=True)
            return

        st.markdown("### Entrar em um time")

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

        if st.button("Entrar no time", use_container_width=True):
            if entrar_no_time(mapa[sel], user_id):
                st.success(f"Voce entrou no time '{sel}'!")
                st.rerun()
            else:
                st.warning("Voce ja pertence a um time.")
