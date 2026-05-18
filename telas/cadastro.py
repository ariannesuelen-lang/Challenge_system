import streamlit as st
import re

from services.auth_service import cadastrar_usuario


def tela_cadastro():

    st.title("Cadastro")

    with st.form("form_cadastro"):

        nome = st.text_input(
            "Nome completo"
        )

        email = st.text_input(
            "E-mail"
        )

        tipo_usuario = st.selectbox(
            "Tipo de usuário",
            [
                "aluno",
                "professor"
            ]
        )

        senha = st.text_input(
            "Senha",
            type="password"
        )

        confirmar = st.text_input(
            "Confirmar senha",
            type="password"
        )

        cadastrar = st.form_submit_button(
            "Cadastrar"
        )

    if cadastrar:

        if (
            not nome
            or not email
            or not senha
        ):

            st.warning(
                "Preencha todos os campos"
            )

        elif not re.match(
            r"[^@]+@[^@]+\.[^@]+",
            email
        ):

            st.warning(
                "E-mail inválido"
            )

        elif senha != confirmar:

            st.error(
                "As senhas não coincidem"
            )

        else:

            resultado = cadastrar_usuario(
                nome,
                email,
                tipo_usuario,
                senha
            )

            if resultado == "ok":

                st.success(
                    "Conta criada com sucesso"
                )

                st.session_state.pagina = "login"

                st.rerun()

            else:

                st.error(resultado)

    st.divider()

    if st.button("Voltar"):

        st.session_state.pagina = "login"

        st.rerun()
