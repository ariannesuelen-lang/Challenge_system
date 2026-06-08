import streamlit as st
from services.desafio_service import listar_desafios
from utils.estilo import aplicar_estilo, cabecalho


def tela_home():

    aplicar_estilo()

    usuario  = st.session_state.get("usuario_logado", {})
    desafios = listar_desafios()

    # Busca segura do nome e tipo de usuário para evitar KeyError na entrada
    nome_usuario = usuario.get("nome") or usuario.get("username") or "Usuário"
    tipo_usuario = usuario.get("tipo_usuario") or usuario.get("perfil") or "aluno"

    cabecalho(
        f"Bem-vindo(a), {nome_usuario}",
        f"Perfil: {tipo_usuario.capitalize()}"
    )

    # --------------------------------------------------
    # DESAFIOS
    # --------------------------------------------------
    with st.expander("Desafios disponiveis", expanded=True):

        if desafios:
            for d in desafios[:5]:
                st.markdown(f"""
                <div style="
                    background:#f0f9ff;
                    border-left:4px solid #00b4d8;
                    border-radius:8px;
                    padding:12px 16px;
                    margin-bottom:8px;
                ">
                    <strong style="color:#0d1b2a;">{d.get('titulo', 'Sem Título')}</strong><br>
                    <span style="color:#555; font-size:13px;">{d.get('descricao','')}</span><br>
                    <span style="color:#00b4d8; font-size:12px;">
                        Nível: {d.get('nivel_dificuldade', d.get('nivel', '-'))} &nbsp;|&nbsp; 
                        Prazo: {d.get('data_limite','-')}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum desafio disponivel no momento.")

        if st.button("Ver todos os desafios", key="home_desafios", width="stretch"):
            st.session_state.pagina = "desafios"
            st.rerun()

    # --------------------------------------------------
    # VOTACAO
    # --------------------------------------------------
    with st.expander("Votacao", expanded=False):

        if desafios:
            for d in desafios[:5]:
                st.markdown(f"""
                <div style="
                    background:#f0f9ff;
                    border-left:4px solid #1b3a5c;
                    border-radius:8px;
                    padding:10px 14px;
                    margin-bottom:6px;
                ">
                    <span style="color:#0d1b2a; font-weight:600;">{d.get('titulo', 'Sem Título')}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhum desafio disponivel para voto.")

        if st.button("Ir para Votacao", key="home_votacao", width="stretch"):
            st.session_state.pagina = "votacao"
            st.rerun()

    # --------------------------------------------------
    # MINI PROVAS
    # --------------------------------------------------
    with st.expander("Mini-provas", expanded=False):

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Provas disponiveis", "—")
        with col2:
            st.metric("Sua pontuacao", "—")

        if st.button("Ir para Mini-provas", key="home_mini", width="stretch"):
            st.session_state.pagina = "mini_provas"
            st.rerun()

    # --------------------------------------------------
    # QUIZ AO VIVO
    # --------------------------------------------------
    with st.expander("Quiz ao Vivo", expanded=False):

        st.markdown("""
        <div style="
            background:#f0f9ff;
            border-left:4px solid #00b4d8;
            border-radius:8px;
            padding:12px 16px;
        ">
            <span style="color:#0d1b2a;">
                Aguarde o professor iniciar um quiz ao vivo.
            </span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Ir para Quiz ao Vivo", key="home_quiz", width="stretch"):
            st.session_state.pagina = "quiz_ao_vivo"
            st.rerun()

    # --------------------------------------------------
    # BATALHA DE EQUIPES
    # --------------------------------------------------
    with st.expander("Batalha de Equipes", expanded=False):

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Batalhas abertas", "—")
        with col2:
            st.metric("Seu time", "—")

        if st.button("Ir para Batalha de Equipes", key="home_batalha", width="stretch"):
            st.session_state.pagina = "batalha_de_equipes"
            st.rerun()
