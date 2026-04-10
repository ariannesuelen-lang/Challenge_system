import streamlit as st
import re
from frontend.api import post


def render():
    st.title("🎓 Sistema Acadêmico")
    aba = st.tabs(["Entrar", "Cadastrar"])

    with aba[0]:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")
        if st.button("Entrar"):
            res = post("/login", {"email": email, "senha": senha})
            if res and res.status_code == 200:
                dados = res.json()
                st.session_state.logado = True
                st.session_state.usuario = dados["usuario"]
                st.success(f"Bem-vindo, {dados['usuario']['nome']}!")
                st.rerun()
            elif res:
                st.error(res.json().get("detail", "Credenciais inválidas"))

    with aba[1]:
        st.subheader("Criar conta")
        nome = st.text_input("Nome completo", key="cad_nome")
        email_c = st.text_input("Email", key="cad_email")
        senha_c = st.text_input("Senha", type="password", key="cad_senha")
        tipo = st.selectbox("Tipo de conta", ["aluno", "professor"], key="cad_tipo")

        campos_preenchidos = all([nome.strip(), email_c.strip(), senha_c.strip()])
        email_valido = re.match(r"[^@]+@[^@]+\.[^@]+", email_c)

        if email_c and not email_valido:
            st.warning("Digite um email válido!")

        senha_criterios = (
            len(senha_c) >= 8 and
            re.search(r"[A-Z]", senha_c) and
            re.search(r"[0-9]", senha_c) and
            re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha_c)
        )

        if senha_c and not senha_criterios:
            st.warning("Senha deve ter pelo menos 8 caracteres, 1 letra maiúscula, 1 número e 1 caractere especial!")

        campos_validos = campos_preenchidos and email_valido and senha_criterios
        placeholder_cadastro = st.empty()

        if st.button("Criar conta", disabled=not campos_validos):
            res = post("/usuarios", {
                "nome": nome,
                "email": email_c,
                "senha": senha_c,
                "tipo_usuario": tipo
            })
            if res is None:
                placeholder_cadastro.error("Não foi possível conectar ao servidor. Tente novamente.")
            elif res.status_code == 200:
                placeholder_cadastro.success("Conta criada! Faça login para continuar.")
            elif res.status_code == 409:
                placeholder_cadastro.error("Este email já está cadastrado!")
            else:
                try:
                    detalhe = res.json().get("detail", "")
                except:
                    detalhe = ""
                placeholder_cadastro.error(detalhe or "Erro ao criar conta.")