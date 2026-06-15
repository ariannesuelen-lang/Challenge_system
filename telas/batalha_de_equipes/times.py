# telas/batalha_de_equipes/times.py
import streamlit as st
from services import batalha_service
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
    # FLUXO DO PROFESSOR (CRIAÇÃO E EDIÇÃO DE TIMES)
    # --------------------------------------------------
    if tipo == "professor":

        st.markdown("### Criar novo time")

        with st.container(border=True):
            nome = st.text_input("Nome do time", placeholder="Ex: Time Alpha")
            if st.button("Criar time", use_container_width=True):
                if not nome or not nome.strip():
                    st.warning("Nome nao pode ser vazio.")
                else:
                    # 🌟 ALTERADO: Chamada via método da classe de serviço
                    if batalha_service.criar_time(nome):
                        st.success(f"Time '{nome}' criado!")
                        st.rerun()
                    else:
                        st.error("Erro ao criar o time.")

        st.divider()
        st.markdown("### Times Cadastrados")

        # 🌟 ALTERADO: Listagem usando a instância global de serviço
        times = batalha_service.listar_times()

        if not times:
            st.info("Nenhum time cadastrado ainda.")
        else:
            for t in times:
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"#### 🛡️ {t.get('nome')}")
                    with col2:
                        # Expander para ações de gerenciamento de cada time
                        with st.expander("Ações", expanded=False):
                            novo_nome = st.text_input(
                                "Novo nome", 
                                value=t.get("nome"), 
                                key=f"edit_nome_{t.get('id')}"
                            )
                            
                            col_b1, col_b2 = st.columns(2)
                            with col_b1:
                                if st.button("Salvar", key=f"salvar_{t.get('id')}"):
                                    # 🌟 ALTERADO: Atualização mapeada na Service
                                    if batalha_service.editar_time(t.get('id'), novo_nome):
                                        st.success("Atualizado!")
                                        st.rerun()
                            with col_b2:
                                if st.button("Excluir", key=f"excluir_{t.get('id')}"):
                                    # 🌟 ALTERADO: Remoção mapeada na Service
                                    if batalha_service.deletar_time(t.get('id')):
                                        st.success("Excluído!")
                                        st.rerun()

    # --------------------------------------------------
    # FLUXO DO ALUNO (ENTRAR EM EQUIPES)
    # --------------------------------------------------
    else:
        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            st.error("Sessão inválida.")
            return

        # 🌟 ALTERADO: Validação inteligente usando a regra de negócio da classe
        if batalha_service.aluno_tem_time(user_id):
            st.markdown("""
            <div style="
                background:#e0f7fa;
                border-left:4px solid #00b4d8;
                border-radius:8px;
                padding:16px 20px;
            ">
                <strong style="color:#0d1b2a;">Você já está associado a um time.</strong><br>
                <span style="color:#555;">Acesse a aba "Integrantes" para visualizar seus colegas de equipe.</span>
            </div>
            """, unsafe_allow_html=True)
            return

        st.markdown("### Entrar em um time")

        # 🌟 ALTERADO: Listagem de times para escolha do estudante
        times = batalha_service.listar_times()

        if not times:
            st.info("Nenhum time disponível no momento para inscrição.")
            return

        mapa = {
            t.get("nome"): t.get("id")
            for t in times
            if isinstance(t, dict) and t.get("nome") and t.get("id")
        }

        if not mapa:
            st.error("Dados inválidos de times.")
            return

        sel = st.selectbox("Selecione um time", list(mapa.keys()))

        if st.button("Confirmar Entrada no Time", use_container_width=True):
            time_id_escolhido = mapa[sel]
            # 🌟 ALTERADO: Registro de entrada utilizando o fluxo seguro da Service
            if batalha_service.entrar_no_time(time_id_escolhido, user_id):
                st.success(f"Você entrou com sucesso no time '{sel}'!")
                st.rerun()
            else:
                st.error("Falha ao entrar no time. Verifique se a vaga ainda está disponível.")