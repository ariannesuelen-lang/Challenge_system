import streamlit as st
from utils.estilo import aplicar_estilo, cabecalho


def tela_batalha_regras():

    aplicar_estilo()
    cabecalho("Regras e Condutas", "Leia com atencao antes de participar")

    if st.button("Voltar"):
        st.session_state.pagina = "batalha_de_equipes"
        st.rerun()

    st.divider()

    with st.expander("Formato da Batalha", expanded=True):
        st.markdown("""
        <div style="color:#0d1b2a; line-height:1.8;">
        <ul>
            <li>O professor cria batalhas com titulo, descricao e prazo.</li>
            <li>Cada aluno envia <strong>uma resposta</strong> por batalha.</li>
            <li>O professor acompanha todas as respostas e finaliza a batalha quando necessario.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Fair Play e Condutas", expanded=False):
        st.markdown("""
        <div style="color:#0d1b2a; line-height:1.8;">
        <ul>
            <li>E proibido copiar respostas de outros participantes.</li>
            <li>Comunicacao durante a batalha deve respeitar as regras definidas pelo professor.</li>
            <li>Todos os integrantes do time devem participar ativamente.</li>
            <li>Respeito mutuo e obrigatorio. Linguagem ofensiva pode gerar penalidade ou desclassificacao.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Penalidades", expanded=False):
        st.markdown("""
        | Infracao | Consequencia |
        |---|---|
        | Trapaca comprovada | Resposta invalidada |
        | Conduta inadequada | Advertencia |
        | Desrespeito | Exclusao da batalha |
        | Nao participacao | Sem pontuacao na rodada |
        """)

    with st.expander("Ideologias", expanded=False):

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div style="
                background:#f0f9ff;
                border-left:4px solid #00b4d8;
                border-radius:8px;
                padding:12px 16px;
                margin-bottom:8px;
            ">
                <strong style="color:#0d1b2a;">Colaboracao vs. Competicao Saudavel</strong><br>
                <span style="color:#555; font-size:13px;">
                    Competir sem perder o espirito de equipe.
                </span>
            </div>
            <div style="
                background:#f0f9ff;
                border-left:4px solid #00b4d8;
                border-radius:8px;
                padding:12px 16px;
            ">
                <strong style="color:#0d1b2a;">Meritocracia com Equilibrio</strong><br>
                <span style="color:#555; font-size:13px;">
                    Pontuacao por desempenho e participacao.
                </span>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="
                background:#f0f9ff;
                border-left:4px solid #1b3a5c;
                border-radius:8px;
                padding:12px 16px;
                margin-bottom:8px;
            ">
                <strong style="color:#0d1b2a;">Papeis no Time</strong><br>
                <span style="color:#555; font-size:13px;">
                    Lider, estrategista, apoio — cada um contribui.
                </span>
            </div>
            <div style="
                background:#f0f9ff;
                border-left:4px solid #1b3a5c;
                border-radius:8px;
                padding:12px 16px;
            ">
                <strong style="color:#0d1b2a;">Decisao sob Pressao</strong><br>
                <span style="color:#555; font-size:13px;">
                    Pensar rapido e em conjunto e a habilidade central.
                </span>
            </div>
            """, unsafe_allow_html=True)
