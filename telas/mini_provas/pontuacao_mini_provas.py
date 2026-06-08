import streamlit as st
from utils.estilo import aplicar_estilo, cabecalho


def tela_pontuacao_mini_provas():

    aplicar_estilo()
    cabecalho("Minha Pontuação", "Veja seu desempenho nas mini-provas")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Pontuação Total", "4.2")
    with col2:
        st.metric("Posição", "1º")

    st.divider()
    st.markdown("### Ranking")

    ranking = [
        {"pos": "1º", "nome": "Eu",  "pts": "5.0", "cor": "#FFD700"},
    ]

    for r in ranking:
        st.markdown(f"""
        <div style="
            background:#f0f9ff;
            border-left:4px solid {r['cor']};
            border-radius:8px;
            padding:10px 16px;
            margin-bottom:6px;
            display:flex;
            justify-content:space-between;
        ">
            <strong style="color:#0d1b2a;">{r['pos']} — {r['nome']}</strong>
            <span style="color:{r['cor']}; font-weight:700;">{r['pts']} pts</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    if st.button("Voltar"):
        st.session_state.pagina = "mini_provas"
        st.rerun()
