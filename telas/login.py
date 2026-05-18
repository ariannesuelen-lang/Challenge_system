import streamlit as st

from services.auth_service import login_usuario


def tela_login():

    st.title("Sistema de Login")

    with st.form("form_login"):

        email = st.text_input("E-mail")

        senha = st.text_input(
            "Senha",
            type="password"
        )

        entrar = st.form_submit_button(
            "Entrar"
        )

    if entrar:

        if not email or not senha:

            st.warning(
                "Preencha todos os campos"
            )

        else:

            usuario = login_usuario(
                email,
                senha
            )

            if usuario:

                st.session_state.usuario_logado = usuario

                st.session_state.pagina = "home"

                st.rerun()

            else:

                st.error(
                    "E-mail ou senha inválidos"
                )

    st.divider()

    if st.button("Criar conta"):

        st.session_state.pagina = "cadastro"

        st.rerun()
