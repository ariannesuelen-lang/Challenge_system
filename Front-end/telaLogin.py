import streamlit as st
import hashlib
import re

st.set_page_config(page_title="Sistema de Login", layout="centered")

# ─────────────────────────────────────────
# CONFIGURAÇÃO DO ADMIN FIXO
# ─────────────────────────────────────────
ADMIN_USUARIO = "admin"
ADMIN_SENHA   = "Admin@123"   # troque aqui quando quiser

# ─────────────────────────────────────────
# BANCO EM MEMÓRIA
# ─────────────────────────────────────────
if "usuarios" not in st.session_state:
    st.session_state.usuarios = [
        {"id": 1, "nome": "João",  "usuario": "joao",  "email": "joao@email.com",  "tipo": "aluno",     "senha": hashlib.sha256("Senha123".encode()).hexdigest()},
        {"id": 2, "nome": "Maria", "usuario": "maria", "email": "maria@email.com", "tipo": "professor", "senha": hashlib.sha256("Senha123".encode()).hexdigest()},
    ]

if "pagina" not in st.session_state:
    st.session_state.pagina = "login"          # login | cadastrar | admin
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None
if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

# ─────────────────────────────────────────
# FUNÇÕES
# ─────────────────────────────────────────
def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def senha_valida(senha):
    if len(senha) < 8:
        return "A senha deve ter no mínimo 8 caracteres"
    if not re.search(r"[A-Z]", senha):
        return "A senha deve conter pelo menos 1 letra maiúscula"
    if not re.search(r"\d", senha):
        return "A senha deve conter pelo menos 1 número"
    return "ok"

def proximo_id():
    ids = [u["id"] for u in st.session_state.usuarios]
    return max(ids) + 1 if ids else 1

def criar_usuario(nome, usuario, email, tipo, senha):
    v = senha_valida(senha)
    if v != "ok":
        return v
    for u in st.session_state.usuarios:
        if u["usuario"] == usuario:
            return "Nome de usuário já existe"
    st.session_state.usuarios.append({
        "id": proximo_id(),
        "nome": nome,
        "usuario": usuario,
        "email": email,
        "tipo": tipo,
        "senha": criptografar_senha(senha),
    })
    return "ok"

def verificar_login(usuario, senha):
    for u in st.session_state.usuarios:
        if u["usuario"] == usuario and u["senha"] == criptografar_senha(senha):
            return u
    return None

def atualizar_usuario(id_usuario, nome, email, tipo, nova_senha):
    for u in st.session_state.usuarios:
        if u["id"] == id_usuario:
            u["nome"]    = nome
            u["email"]   = email
            u["tipo"]    = tipo
            if nova_senha:
                v = senha_valida(nova_senha)
                if v != "ok":
                    return v
                u["senha"] = criptografar_senha(nova_senha)
            return "ok"
    return "Usuário não encontrado"

def remover_usuario(id_usuario):
    st.session_state.usuarios = [
        u for u in st.session_state.usuarios if u["id"] != id_usuario
    ]

# ─────────────────────────────────────────
# BARRA LATERAL
# ─────────────────────────────────────────
with st.sidebar:
    st.title("📋 Menu")

    if st.session_state.admin_logado:
        st.success("🛡️ Admin logado")
        if st.button("🚪 Sair do Admin"):
            st.session_state.admin_logado = False
            st.session_state.pagina = "login"
            st.rerun()
    elif st.session_state.usuario_logado:
        u = st.session_state.usuario_logado
        st.success(f"👤 {u['nome']}")
        if st.button("🚪 Sair"):
            st.session_state.usuario_logado = None
            st.session_state.pagina = "login"
            st.rerun()
    else:
        if st.button("🔑 Login",     use_container_width=True):
            st.session_state.pagina = "login";      st.rerun()
        if st.button("📝 Cadastrar", use_container_width=True):
            st.session_state.pagina = "cadastrar";  st.rerun()

    st.markdown("---")

    # Botão que abre o modal de acesso admin
    if not st.session_state.admin_logado:
        if st.button("🛡️ Acesso Administrativo", use_container_width=True):
            st.session_state.pagina = "admin_login"
            st.rerun()

# ─────────────────────────────────────────
# PÁGINA: LOGIN
# ─────────────────────────────────────────
if st.session_state.pagina == "login":
    st.title("🔑 Sistema de Login")

    if st.session_state.usuario_logado:
        u = st.session_state.usuario_logado
        st.success(f"Bem-vindo(a), **{u['nome']}**! ({u['tipo']})")
        st.info(f"📧 {u['email']}")
    else:
        with st.form("form_login"):
            st.subheader("Entrar")
            usuario = st.text_input("Usuário")
            senha   = st.text_input("Senha", type="password")
            entrar  = st.form_submit_button("Entrar", use_container_width=True)

        if entrar:
            encontrado = verificar_login(usuario, senha)
            if encontrado:
                st.session_state.usuario_logado = encontrado
                st.success(f"Bem-vindo(a), {encontrado['nome']}!")
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos")

# ─────────────────────────────────────────
# PÁGINA: CADASTRO
# ─────────────────────────────────────────
elif st.session_state.pagina == "cadastrar":
    st.title("📝 Criar Conta")

    with st.form("form_cadastro"):
        nome    = st.text_input("Nome completo")
        usuario = st.text_input("Nome de usuário")
        email   = st.text_input("E-mail")
        tipo    = st.selectbox("Tipo", ["aluno", "professor"])
        senha   = st.text_input("Senha", type="password")
        st.caption("Mínimo 8 caracteres, 1 maiúscula, 1 número")
        cadastrar = st.form_submit_button("Criar conta", use_container_width=True)

    if cadastrar:
        if not nome or not usuario or not email:
            st.warning("Preencha todos os campos")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.warning("E-mail inválido")
        else:
            resultado = criar_usuario(nome, usuario, email, tipo, senha)
            if resultado == "ok":
                st.success("Conta criada com sucesso! Faça o login.")
            else:
                st.error(resultado)

# ─────────────────────────────────────────
# PÁGINA: LOGIN DO ADMIN
# ─────────────────────────────────────────
elif st.session_state.pagina == "admin_login":
    st.title("🛡️ Acesso Administrativo")

    with st.form("form_admin_login"):
        st.info("Área restrita. Insira as credenciais de administrador.")
        adm_user  = st.text_input("Usuário admin")
        adm_senha = st.text_input("Senha admin", type="password")
        col1, col2 = st.columns(2)
        entrar    = col1.form_submit_button("Entrar", use_container_width=True)
        cancelar  = col2.form_submit_button("Cancelar", use_container_width=True)

    if entrar:
        if adm_user == ADMIN_USUARIO and adm_senha == ADMIN_SENHA:
            st.session_state.admin_logado = True
            st.session_state.pagina = "admin"
            st.rerun()
        else:
            st.error("Credenciais inválidas")

    if cancelar:
        st.session_state.pagina = "login"
        st.rerun()

# ─────────────────────────────────────────
# PÁGINA: PAINEL ADMIN
# ─────────────────────────────────────────
elif st.session_state.pagina == "admin":
    if not st.session_state.admin_logado:
        st.warning("Acesso negado. Faça login como administrador.")
        st.session_state.pagina = "admin_login"
        st.rerun()

    st.title("🛡️ Painel Administrativo")
    usuarios = st.session_state.usuarios

    if not usuarios:
        st.warning("Nenhum usuário cadastrado.")
    else:
        # Seletor de usuário
        opcoes = {f"{u['nome']} — {u['usuario']} ({u['email']})": u for u in usuarios}
        selecionado = st.selectbox("Selecione um usuário", list(opcoes.keys()))
        usuario = opcoes[selecionado]

        st.markdown("---")
        st.subheader(f"Editando: {usuario['nome']}")

        with st.form("form_admin_edit"):
            nome  = st.text_input("Nome",    value=usuario["nome"])
            email = st.text_input("E-mail",  value=usuario["email"])
            tipo  = st.selectbox(
                "Tipo",
                ["aluno", "professor"],
                index=0 if usuario["tipo"] == "aluno" else 1
            )
            nova_senha = st.text_input("Nova senha (deixe em branco para não alterar)", type="password")

            col1, col2 = st.columns(2)
            salvar  = col1.form_submit_button("💾 Salvar",  use_container_width=True)
            deletar = col2.form_submit_button("🗑️ Deletar", use_container_width=True)

        # Validações inline (fora do form)
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.warning("E-mail inválido!")

        if nova_senha:
            senha_ok = (
                len(nova_senha) >= 8 and
                re.search(r"[A-Z]", nova_senha) and
                re.search(r"[0-9]", nova_senha)
            )
            if not senha_ok:
                st.warning("Senha fraca! Mínimo 8 caracteres, 1 maiúscula e 1 número.")

        if salvar:
            resultado = atualizar_usuario(usuario["id"], nome, email, tipo, nova_senha)
            if resultado == "ok":
                st.success("Usuário atualizado com sucesso!")
                st.rerun()
            else:
                st.error(resultado)

        if deletar:
            remover_usuario(usuario["id"])
            st.warning("Usuário removido.")
            st.rerun()

    # Lista rápida de todos os usuários
    st.markdown("---")
    st.subheader("📋 Todos os usuários")
    for u in st.session_state.usuarios:
        st.markdown(f"- **{u['nome']}** (`{u['usuario']}`) — {u['tipo']} — {u['email']}")
