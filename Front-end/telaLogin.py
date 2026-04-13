import streamlit as st
import re

st.set_page_config(page_title="Admin", layout="centered")

st.title("🛡️ Painel Administrativo (Simples)")

# =========================
# BANCO FAKE (simulação)
# =========================
usuarios = [
    {"id": 1, "nome": "João", "email": "joao@email.com", "tipo": "aluno"},
    {"id": 2, "nome": "Maria", "email": "maria@email.com", "tipo": "professor"},
]

# =========================
# SELEÇÃO DE USUÁRIO
# =========================
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

    salvar = st.form_submit_button("💾 Salvar")

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

    st.write("📌 Dados atualizados:")
    st.json(usuario)
