# telas/mini_provas/desempenho_mini_provas.py
import streamlit as st

def tela_desempenho_mini_provas():
    st.title("Meu Desempenho")
    st.metric("Média Geral", "7.8")
    st.metric("Tempo Médio", "42s")
    st.metric("Taxa de Acertos", "78%")

    st.divider()
    st.subheader("Disciplinas")
    st.write("Banco de dados: 8.0")
    st.write("Lab de Software: 7.5")

    st.divider()
    if st.button("Voltar"):
        # 🌟 ALTERADO: Navegação limpa via state
        st.session_state.pagina = "mini_provas"
        st.rerun()