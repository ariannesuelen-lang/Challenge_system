# telas/mini_provas/resultado_mini_prova.py
import streamlit as st

def tela_resultado_mini_prova():
    st.title("Resultado da Mini Prova")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Nota", "8.0")
    with col2:
        st.metric("Pontuação", "0.8")
    with col3:
        st.metric("Acertos", "4/5")

    st.divider()
    st.subheader("Questões")

    for i in range(5):
        with st.container(border=True):
            st.write(f"Questão {i+1}")
            if i == 4:
                st.error("❌ Resposta incorreta (Alternativa marcada: B | Correta: D)")
            else:
                st.success("✅ Resposta correta")

    st.divider()
    if st.button("Voltar"):
        # 🌟 ALTERADO: Agora volta explicitamente para a lista do histórico renomeado
        st.session_state.pagina = "historico_provas"
        st.rerun()