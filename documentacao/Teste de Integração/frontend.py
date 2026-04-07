import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

# =========================
# ESTADO DE SESSÃO
# =========================

if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# =========================
# HELPERS
# =========================

def get(endpoint, params=None):
    try:
        res = requests.get(f"{BASE_URL}{endpoint}", params=params)
        return res.json() if res.status_code == 200 else []
    except:
        return []

def post(endpoint, body):
    try:
        return requests.post(f"{BASE_URL}{endpoint}", json=body)
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None

def put(endpoint, body, params=None):
    try:
        return requests.put(f"{BASE_URL}{endpoint}", json=body, params=params)
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None

def delete(endpoint, params=None):
    try:
        return requests.delete(f"{BASE_URL}{endpoint}", params=params)
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None

def is_professor():
    return st.session_state.usuario and st.session_state.usuario["tipo_usuario"] == "professor"

def user_id():
    return st.session_state.usuario["id"]

# =========================
# TELA DE LOGIN / CADASTRO
# =========================

def tela_acesso():
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
        if st.button("Criar conta"):
            res = post("/usuarios", {"nome": nome, "email": email_c, "senha": senha_c, "tipo_usuario": tipo})
            if res and res.status_code == 200:
                st.success("Conta criada! Faça login para continuar.")
            elif res:
                st.error(res.json().get("detail", "Erro ao criar conta"))

# =========================
# PÁGINAS
# =========================

def pagina_desafios():
    st.subheader("📋 Desafios")

    # Filtro por disciplina
    disciplinas = get("/disciplinas")
    opcoes_disc = {"Todas": None}
    opcoes_disc.update({d["nome"]: d["id"] for d in disciplinas})
    filtro = st.selectbox("Filtrar por disciplina", list(opcoes_disc.keys()))
    disc_id = opcoes_disc[filtro]

    desafios = get("/desafios", params={"disciplina_id": disc_id} if disc_id else None)

    if not desafios:
        st.info("Nenhum desafio encontrado.")
        return

    for d in desafios:
        with st.expander(f"📌 {d['titulo']} — {d.get('disciplina_nome', 'Sem disciplina')}"):
            st.write(f"**Criado por:** {d['criador_nome']}")
            if d.get("descricao"):
                st.write(f"**Descrição:** {d['descricao']}")
            if d.get("data_limite"):
                st.write(f"**Prazo:** {d['data_limite'][:10]}")

            st.markdown("---")
            st.markdown("**💬 Respostas:**")

            respostas = get(f"/desafios/{d['id']}/respostas")
            if respostas:
                for r in respostas:
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"👤 **{r['usuario_nome']}:** {r['conteudo']}")
                    with col2:
                        votos = r.get("total_votos", 0)
                        if st.button(f"👍 {votos}", key=f"voto_{r['id']}"):
                            res = post("/votos", {"resposta_id": r["id"], "usuario_id": user_id()})
                            if res and res.status_code == 200:
                                st.success("Voto registrado!")
                                st.rerun()
                            elif res:
                                st.warning(res.json().get("detail"))
            else:
                st.info("Nenhuma resposta ainda. Seja o primeiro!")

            st.markdown("---")
            with st.form(key=f"form_resp_{d['id']}"):
                conteudo = st.text_area("Sua resposta", key=f"resp_{d['id']}")
                if st.form_submit_button("Enviar resposta"):
                    res = post("/respostas", {
                        "desafio_id": d["id"],
                        "usuario_id": user_id(),
                        "conteudo": conteudo
                    })
                    if res and res.status_code == 200:
                        st.success("Resposta enviada!")
                        st.rerun()
                    elif res:
                        st.error(res.json().get("detail"))


def pagina_criar_desafio():
    st.subheader("➕ Criar Desafio")

    disciplinas = get("/disciplinas")
    opcoes = {"(Nenhuma)": None}
    opcoes.update({d["nome"]: d["id"] for d in disciplinas})

    titulo = st.text_input("Título do desafio")
    descricao = st.text_area("Descrição (opcional)")
    disc_sel = st.selectbox("Disciplina", list(opcoes.keys()))
    data_limite = st.date_input("Data limite (opcional)", value=None)

    if st.button("Criar Desafio"):
        res = post("/desafios", {
            "titulo": titulo,
            "descricao": descricao,
            "criador_id": user_id(),
            "disciplina_id": opcoes[disc_sel],
            "data_limite": str(data_limite) if data_limite else None
        })
        if res and res.status_code == 200:
            st.success("Desafio criado com sucesso!")
        elif res:
            st.error(res.json().get("detail"))


def pagina_gerenciar_desafios():
    st.subheader("✏️ Gerenciar Desafios")

    desafios = get("/desafios")
    meus = [d for d in desafios if d["criador_id"] == user_id()]

    if not meus:
        st.info("Você ainda não criou nenhum desafio.")
        return

    opcoes = {f"ID {d['id']} — {d['titulo']}": d for d in meus}
    sel = st.selectbox("Selecione o desafio", list(opcoes.keys()))
    desafio = opcoes[sel]

    disciplinas = get("/disciplinas")
    opts_disc = {"(Nenhuma)": None}
    opts_disc.update({d["nome"]: d["id"] for d in disciplinas})

    titulo = st.text_input("Título", value=desafio["titulo"])
    descricao = st.text_area("Descrição", value=desafio.get("descricao", ""))
    disc_atual = next((k for k, v in opts_disc.items() if v == desafio.get("disciplina_id")), "(Nenhuma)")
    disc_sel = st.selectbox("Disciplina", list(opts_disc.keys()), index=list(opts_disc.keys()).index(disc_atual))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Atualizar"):
            res = put(f"/desafios/{desafio['id']}", {
                "titulo": titulo,
                "descricao": descricao,
                "disciplina_id": opts_disc[disc_sel],
                "data_limite": desafio.get("data_limite")
            }, params={"usuario_id": user_id()})
            if res and res.status_code == 200:
                st.success("Desafio atualizado!")
                st.rerun()
            elif res:
                st.error(res.json().get("detail"))
    with col2:
        if st.button("🗑️ Deletar"):
            res = delete(f"/desafios/{desafio['id']}", params={"usuario_id": user_id()})
            if res and res.status_code == 200:
                st.warning("Desafio deletado.")
                st.rerun()
            elif res:
                st.error(res.json().get("detail"))


def pagina_cursos_disciplinas():
    st.subheader("🏫 Cursos e Disciplinas")

    aba = st.tabs(["Cursos", "Disciplinas"])

    with aba[0]:
        cursos = get("/cursos")
        if cursos:
            for c in cursos:
                st.write(f"📘 **{c['nome']}** (ID: {c['id']})")
        else:
            st.info("Nenhum curso cadastrado.")

        if is_professor():
            st.markdown("---")
            nome_curso = st.text_input("Nome do novo curso")
            if st.button("Criar Curso"):
                res = post("/cursos", {"nome": nome_curso})
                if res and res.status_code == 200:
                    st.success("Curso criado!")
                    st.rerun()

    with aba[1]:
        disciplinas = get("/disciplinas")
        if disciplinas:
            for d in disciplinas:
                st.write(f"📗 **{d['nome']}** — Curso: {d['curso_nome']} (ID: {d['id']})")
        else:
            st.info("Nenhuma disciplina cadastrada.")

        if is_professor():
            st.markdown("---")
            cursos = get("/cursos")
            opts_curso = {c["nome"]: c["id"] for c in cursos}
            nome_disc = st.text_input("Nome da nova disciplina")
            if opts_curso:
                curso_sel = st.selectbox("Curso", list(opts_curso.keys()))
                if st.button("Criar Disciplina"):
                    res = post("/disciplinas", {"nome": nome_disc, "curso_id": opts_curso[curso_sel]})
                    if res and res.status_code == 200:
                        st.success("Disciplina criada!")
                        st.rerun()
            else:
                st.warning("Cadastre um curso antes de criar disciplinas.")

# =========================
# SISTEMA PRINCIPAL
# =========================

def sistema():
    usuario = st.session_state.usuario
    tipo = usuario["tipo_usuario"]

    st.sidebar.title(f"👤 {usuario['nome']}")
    st.sidebar.caption(f"{tipo.capitalize()}")

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.session_state.usuario = None
        st.rerun()

    st.sidebar.markdown("---")

    opcoes = ["📋 Desafios", "🏫 Cursos e Disciplinas"]
    if tipo == "professor":
        opcoes += ["➕ Criar Desafio", "✏️ Gerenciar Desafios"]

    menu = st.sidebar.radio("Navegação", opcoes)

    if menu == "📋 Desafios":
        pagina_desafios()
    elif menu == "🏫 Cursos e Disciplinas":
        pagina_cursos_disciplinas()
    elif menu == "➕ Criar Desafio":
        pagina_criar_desafio()
    elif menu == "✏️ Gerenciar Desafios":
        pagina_gerenciar_desafios()

# =========================
# ENTRADA
# =========================

if not st.session_state.logado:
    tela_acesso()
else:
    sistema()
