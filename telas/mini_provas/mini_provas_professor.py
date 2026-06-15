# telas/mini_provas/mini_provas_professor.py
import streamlit as st
# 🌟 ALTERADO: Puxando a instância única global do serviço
from services import mini_prova_service
from utils.estilo import aplicar_estilo, cabecalho


def tela_mini_provas_professor():
    aplicar_estilo()
    cabecalho("Painel do Professor", "Gerencie mini provas e perguntas")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Cadastrar Perguntas", use_container_width=True):
            st.session_state.pagina = "cadastro_perguntas"
            st.rerun()

    with col2:
        if st.button("Cadastrar Mini Prova", use_container_width=True):
            st.session_state.pagina = "cadastro_mini_provas"
            st.rerun()

    with col3:
        if st.button("Ver Perguntas", use_container_width=True):
            st.session_state.pagina = "lista_perguntas"
            st.rerun()

    st.divider()
    st.markdown("### Mini Provas Criadas")

    # 🌟 ALTERADO: Consumo mapeado na classe de serviços
    mini_provas = mini_prova_service.listar_mini_provas()

    if not mini_provas:
        st.info("Nenhuma mini prova cadastrada ainda.")
        return

    for prova in mini_provas:
        with st.container(border=True):
            # 🌟 ALTERADO: Nomenclaturas das chaves adaptadas para as colunas corrigidas no banco PT-BR
            st.markdown(f"""
            <div style="
                border-left:4px solid #00b4d8;
                padding-left:12px;
                margin-bottom:8px;
            ">
                <strong style="color:#0d1b2a; font-size:16px;">
                    {prova.get('titulo', 'Sem título')}
                </strong><br>
                <span style="color:#555; font-size:13px;">
                    {prova.get('descricao', '')}
                </span><br>
                <span style="color:#00b4d8; font-size:12px;">
                    {prova.get('quantidade_questoes', '-')} questões
                    &nbsp;|&nbsp;
                    {prova.get('duracao_minutos', '-')} min
                </span>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Editar", key=f"editar_{prova['id']}", use_container_width=True):
                    st.session_state.id_mini_prova = prova["id"]
                    st.session_state.pagina = "editar_mini_prova"
                    st.rerun()

            with col2:
                if st.button("Visualizar", key=f"visualizar_{prova['id']}", use_container_width=True):
                    st.session_state.id_mini_prova = prova["id"]
                    st.session_state.pagina = "visualizar_mini_prova"
                    st.rerun()