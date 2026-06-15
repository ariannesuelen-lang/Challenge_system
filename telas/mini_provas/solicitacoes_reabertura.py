import streamlit as st


def tela_solicitacoes_reabertura():

    st.title("Solicitações de Reabertura")

    for i in range(2):

        with st.container(border=True):

            st.write("Aluno: João")

            st.write(
                "Motivo: minha internet caiu"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(f"Aprovar {i}"):
                    st.success("Solicitação aprovada")

            with col2:

                if st.button(f"Recusar {i}"):
                    st.error("Solicitação recusada")

    st.divider()

    if st.button("Voltar"):

        st.switch_page(
            "telas/mini_provas/mini_provas_professor.py"
        )
