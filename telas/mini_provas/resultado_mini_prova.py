import streamlit as st


def tela_resultado_mini_prova():

    st.title("Resultado da Mini Prova")

    st.metric("Nota", "8.0")

    st.metric("Pontuação", "0.8")

    st.metric("Acertos", "4/5")

    st.divider()

    st.subheader("Questões")

    for i in range(5):

        with st.container(border=True):

            st.write(f"Questão {i+1}")

            st.success("Resposta correta")

    st.divider()

    if st.button("Voltar"):

        st.switch_page(
            "telas/mini_provas/resultados_mini_provas.py"
        )
