import streamlit as st
import re
from services.auth_service import cadastrar_usuario
from utils.estilo import aplicar_estilo, cabecalho


def tela_cadastro():

    aplicar_estilo()
    cabecalho("Criar conta", "Preencha os dados para se cadastrar")

    col_esq, col_centro, col_dir = st.columns([1, 2, 1])

    with col_centro:

        with st.form("form_cadastro"):

            nome = st.text_input("Nome completo", placeholder="Seu nome")
            email = st.text_input("E-mail", placeholder="seu@email.com")

            tipo_usuario = st.selectbox(
                "Tipo de usuario",
                ["aluno", "professor"],
                format_func=lambda x: x.capitalize()
            )

            senha    = st.text_input("Senha", type="password", placeholder="••••••••")
            confirmar = st.text_input("Confirmar senha", type="password", placeholder="••••••••")

            st.markdown("<br>", unsafe_allow_html=True)
            cadastrar = st.form_submit_button("Cadastrar", use_container_width=True)

        if cadastrar:

            if not nome or not email or not senha:
                st.warning("Preencha todos os campos.")

            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.warning("E-mail invalido.")

            elif senha != confirmar:
                st.error("As senhas nao coincidem.")

            else:
                resultado = cadastrar_usuario(nome, email, tipo_usuario, senha)

                if resultado == "ok":
                    st.success("Conta criada com sucesso!")
                    st.session_state.pagina = "login"
                    st.rerun()
                else:
                    st.error(resultado)

        st.divider()

        if st.button("Voltar para o login", use_container_width=True):
            st.session_state.pagina = "login"
            st.rerun()
