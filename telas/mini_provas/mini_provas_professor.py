import streamlit as st


def tela_mini_provas_professor():

    st.title("Painel de Mini Provas")

    st.subheader("Área do Professor")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Cadastrar Perguntas"):
            st.switch_page(
                "telas/mini_provas/cadastro_perguntas.py"
            )

        if st.button("Cadastrar Mini Prova"):
            st.switch_page(
                "telas/mini_provas/cadastro_mini_provas.py"
            )

    with col2:

        if st.button("Solicitações de Reabertura"):
            st.switch_page(
                "telas/mini_provas/solicitacoes_reabertura.py"
            )

        if st.button("Notificações"):
            st.switch_page(
                "telas/mini_provas/notificacoes_mini_provas.py"
            )

    st.divider()

    st.subheader("Mini Provas Criadas")

    st.info(
        "Aqui futuramente aparecerão as mini provas cadastradas"
    )
