import streamlit as st
import re

st.set_page_config(page_title="Admin", layout="centered")

st.title("🛡️ Painel Administrativo (Simples)")

# =========================
# BANCO FAKE (simulação)
# =========================
if "usuarios" not in st.session_state:
    st.session_state.usuarios = [
        {"id": 1, "nome": "João", "email": "joao@email.com", "tipo": "aluno"},
        {"id": 2, "nome": "Maria", "email": "maria@email.com", "tipo": "professor"},
    ]

usuarios = st.session_state.usuarios

# =========================
# SELEÇÃO DE USUÁRIO
# =========================
if not usuarios:
    st.warning("Nenhum usuário cadastrado.")
    st.stop()

opcoes = {f"{u['nome']} ({u['email']})": u for u in usuarios}
selecionado = st.selectbox("Selecione um usuário", list(opcoes.keys()))

usuario = opcoes[selecionado]

st.markdown("---")

# =========================
# FORMULÁRIO
# =========================
with st.form("form_admin"):
    nome = st.text_input("Nome", value=usuario["nome"])
    email = st.text_input("Email", value=usuario["email"])
    
    tipo = st.selectbox(
        "Tipo de usuário",
        ["aluno", "professor"],
        index=0 if usuario["tipo"] == "aluno" else 1
    )

    senha = st.text_input("Nova senha", type="password")

    col1, col2 = st.columns(2)
    salvar = col1.form_submit_button("💾 Salvar")
    deletar = col2.form_submit_button("🗑️ Deletar")

# =========================
# VALIDAÇÕES
# =========================
if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    st.warning("Email inválido!")

if senha:
    senha_ok = (
        len(senha) >= 8 and
        re.search(r"[A-Z]", senha) and
        re.search(r"[0-9]", senha) and
        re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha)
    )
    if not senha_ok:
        st.warning("Senha fraca!")

# =========================
# SALVAR ALTERAÇÕES
# =========================
if salvar:
    usuario["nome"] = nome
    usuario["email"] = email
    usuario["tipo"] = tipo

    st.success("Usuário atualizado com sucesso!")
    st.rerun()

# =========================
# DELETAR USUÁRIO
# =========================
if deletar:
    st.session_state.usuarios = [u for u in usuarios if u["id"] != usuario["id"]]

    st.warning("Usuário deletado!")
    st.rerun()
