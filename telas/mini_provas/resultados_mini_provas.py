import streamlit as st


def tela_resultados_mini_provas():

    st.title("Resultados")

    st.subheader("Mini provas finalizadas")

    for i in range(3):

        with st.container(border=True):

            st.write(f"Mini Prova {i+1}")
            st.write("Nota: 8.0")
            st.write("Pontuação: 0.8")

            if st.button(
                f"Ver resultado {i}"
            ):

                st.switch_page(
                    "telas/mini_provas/resultado_mini_prova.py"
                )

    st.divider()

    if st.button("Voltar"):

        st.switch_page(
            "telas/mini_provas/mini_provas.py"
        )
