import streamlit as st
import hashlib
import re
from supabase import create_client, Client

st.set_page_config(page_title="Sistema de Login", layout="centered")

# ─────────────────────────────────────────
# CONEXÃO COM SUPABASE
# ─────────────────────────────────────────
@st.cache_resource
def get_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = get_supabase()

# ─────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────
if "pagina" not in st.session_state:
    st.session_state.pagina = "login"
if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None
if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

# ─────────────────────────────────────────
# FUNÇÕES UTILITÁRIAS
# ─────────────────────────────────────────
def criptografar_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def senha_valida(senha: str) -> str:
    if len(senha) < 8:
        return "A senha deve ter no mínimo 8 caracteres"
    if not re.search(r"[A-Z]", senha):
        return "A senha deve conter pelo menos 1 letra maiúscula"
    if not re.search(r"\d", senha):
        return "A senha deve conter pelo menos 1 número"
    return "ok"

# ─────────────────────────────────────────
# FUNÇÕES — TABELA: usuarios
# Colunas: id, nome, email, senha, tipo_usuario, criado_em
# ─────────────────────────────────────────
def verificar_login_usuario(email: str, senha: str):
    """Login pelo e-mail (campo único identificador na tabela usuarios)."""
    res = (
        supabase.table("usuarios")
        .select("id, nome, email, tipo_usuario, criado_em")
        .eq("email", email)
        .eq("senha", criptografar_senha(senha))
        .execute()
    )
    return res.data[0] if res.data else None

def criar_usuario(nome: str, email: str, tipo_usuario: str, senha: str) -> str:
    v = senha_valida(senha)
    if v != "ok":
        return v
    existe = supabase.table("usuarios").select("id").eq("email", email).execute()
    if existe.data:
        return "E-mail já cadastrado"
    supabase.table("usuarios").insert({
        "nome":         nome,
        "email":        email,
        "tipo_usuario": tipo_usuario,
        "senha":        criptografar_senha(senha),
    }).execute()
    return "ok"

def listar_usuarios():
    res = (
        supabase.table("usuarios")
        .select("id, nome, email, tipo_usuario, criado_em")
        .order("id")
        .execute()
    )
    return res.data or []

def atualizar_usuario(id_usuario: int, nome: str, email: str, tipo_usuario: str, nova_senha: str) -> str:
    dados = {"nome": nome, "email": email, "tipo_usuario": tipo_usuario}
    if nova_senha:
        v = senha_valida(nova_senha)
        if v != "ok":
            return v
        dados["senha"] = criptografar_senha(nova_senha)
    supabase.table("usuarios").update(dados).eq("id", id_usuario).execute()
    return "ok"

def remover_usuario(id_usuario: int):
    supabase.table("usuarios").delete().eq("id", id_usuario).execute()

# ─────────────────────────────────────────
# FUNÇÕES — TABELA: adm
# Colunas: id, email, senha, nome
# ─────────────────────────────────────────
def verificar_login_admin(email: str, senha: str):
    """Login do admin via tabela 'adm'."""
    res = (
        supabase.table("adm")
        .select("id, nome, email")
        .eq("email", email)
        .eq("senha", criptografar_senha(senha))
        .execute()
    )
    return res.data[0] if res.data else None

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
        if st.button("🔑 Login", use_container_width=True):
            st.session_state.pagina = "login"
            st.rerun()
        if st.button("📝 Cadastrar", use_container_width=True):
            st.session_state.pagina = "cadastrar"
            st.rerun()

    st.markdown("---")

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
        st.success(f"Bem-vindo(a), **{u['nome']}**! ({u['tipo_usuario']})")
        st.info(f"📧 {u['email']}")
    else:
        with st.form("form_login"):
            st.subheader("Entrar")
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            entrar = st.form_submit_button("Entrar", use_container_width=True)

        if entrar:
            if not email or not senha:
                st.warning("Preencha todos os campos")
            else:
                encontrado = verificar_login_usuario(email, senha)
                if encontrado:
                    st.session_state.usuario_logado = encontrado
                    st.success(f"Bem-vindo(a), {encontrado['nome']}!")
                    st.rerun()
                else:
                    st.error("E-mail ou senha inválidos")

# ─────────────────────────────────────────
# PÁGINA: CADASTRO
# ─────────────────────────────────────────
elif st.session_state.pagina == "cadastrar":
    st.title("📝 Criar Conta")

    with st.form("form_cadastro"):
        nome          = st.text_input("Nome completo")
        email         = st.text_input("E-mail")
        tipo_usuario  = st.selectbox("Tipo", ["aluno", "professor"])
        senha         = st.text_input("Senha", type="password")
        st.caption("Mínimo 8 caracteres, 1 maiúscula, 1 número")
        cadastrar = st.form_submit_button("Criar conta", use_container_width=True)

    if cadastrar:
        if not nome or not email:
            st.warning("Preencha todos os campos")
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.warning("E-mail inválido")
        else:
            resultado = criar_usuario(nome, email, tipo_usuario, senha)
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
        adm_email = st.text_input("E-mail admin")
        adm_senha = st.text_input("Senha admin", type="password")
        col1, col2 = st.columns(2)
        entrar   = col1.form_submit_button("Entrar",   use_container_width=True)
        cancelar = col2.form_submit_button("Cancelar", use_container_width=True)

    if entrar:
        admin = verificar_login_admin(adm_email, adm_senha)
        if admin:
            st.session_state.admin_logado = True
            st.session_state.admin_info   = admin  # guarda nome/email do admin
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

    admin_info = st.session_state.get("admin_info", {})
    st.title("🛡️ Painel Administrativo")
    if admin_info:
        st.caption(f"Logado como: **{admin_info.get('nome', '')}** — {admin_info.get('email', '')}")

    usuarios = listar_usuarios()

    if not usuarios:
        st.warning("Nenhum usuário cadastrado.")
    else:
        opcoes = {
            f"{u['nome']} ({u['email']}) — {u['tipo_usuario']}": u
            for u in usuarios
        }
        selecionado = st.selectbox("Selecione um usuário", list(opcoes.keys()))
        usuario = opcoes[selecionado]

        st.markdown("---")
        st.subheader(f"Editando: {usuario['nome']}")

        with st.form("form_admin_edit"):
            nome         = st.text_input("Nome",   value=usuario["nome"])
            email        = st.text_input("E-mail", value=usuario["email"])
            tipo_usuario = st.selectbox(
                "Tipo",
                ["aluno", "professor"],
                index=0 if usuario["tipo_usuario"] == "aluno" else 1,
            )
            nova_senha = st.text_input(
                "Nova senha (deixe em branco para não alterar)", type="password"
            )
            col1, col2 = st.columns(2)
            salvar  = col1.form_submit_button("💾 Salvar",   use_container_width=True)
            deletar = col2.form_submit_button("🗑️ Deletar",  use_container_width=True)

        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            st.warning("E-mail inválido!")

        if nova_senha:
            senha_ok = (
                len(nova_senha) >= 8
                and re.search(r"[A-Z]", nova_senha)
                and re.search(r"[0-9]", nova_senha)
            )
            if not senha_ok:
                st.warning("Senha fraca! Mínimo 8 caracteres, 1 maiúscula e 1 número.")

        if salvar:
            resultado = atualizar_usuario(usuario["id"], nome, email, tipo_usuario, nova_senha)
            if resultado == "ok":
                st.success("Usuário atualizado com sucesso!")
                st.rerun()
            else:
                st.error(resultado)

        if deletar:
            remover_usuario(usuario["id"])
            st.warning("Usuário removido.")
            st.rerun()

    st.markdown("---")
    st.subheader("📋 Todos os usuários")
    for u in listar_usuarios():
        st.markdown(
            f"- **{u['nome']}** — `{u['email']}` — {u['tipo_usuario']}"
            + (f" _(criado em {u['criado_em'][:10]})_" if u.get("criado_em") else "")
        )