import streamlit as st
from utils.estilo import aplicar_estilo, cabecalho


def tela_realizar_mini_prova():

    aplicar_estilo()
    cabecalho("Realizar Mini Prova", "Leia as instruções antes de começar")

    st.markdown("""
    <div style="
        background:#fff3e0;
        border-left:4px solid #ff9800;
        border-radius:8px;
        padding:14px 18px;
        margin-bottom:16px;
    ">
        <strong style="color:#0d1b2a;">Atenção antes de iniciar:</strong>
        <ul style="color:#555; margin:8px 0 0; padding-left:18px;">
            <li>O tempo começará imediatamente;</li>
            <li>Você não poderá sair da tela;</li>
            <li>Caso saia, a prova será encerrada;</li>
            <li>Somente o professor poderá liberar nova tentativa.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Começar", use_container_width=True):
        st.success("Mini prova iniciada!")
        st.markdown("### Questão 1")
        st.radio(
            "Escolha uma alternativa",
            ["Alternativa A", "Alternativa B", "Alternativa C", "Alternativa D", "Alternativa E"]
        )
        st.progress(20)

    st.divider()
    if st.button("Voltar"):
        st.session_state.pagina = "mini_provas"
        st.rerun()
