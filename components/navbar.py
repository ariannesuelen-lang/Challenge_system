import streamlit as st

def mostrar_menu():
    pagina_atual = st.session_state.get("pagina", "home")
    usuario = st.session_state.usuario_logado

    st.markdown("""
        <style>
        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            text-align: left;
            background-color: transparent;
            border: none;
            color: inherit;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            transition: background-color 0.2s;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: rgba(255,255,255,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    paginas_keys = {
        "home": "menu_home",
        "desafios": "menu_desafios",
        "votacao": "menu_votacao",
        "mini_provas": "menu_miniprovas",
        "quiz_ao_vivo": "menu_quiz_ao_vivo",
        "batalha_de_equipes": "menu_batalha_de_equipes",
        "admin": "menu_admin",
    }

    key_ativo = paginas_keys.get(pagina_atual, "")

    if key_ativo:
        st.markdown(f"""
            <style>
            [data-testid="stSidebar"] [data-testid="stButton-{key_ativo}"] > button {{
                background-color: rgba(255,255,255,0.15) !important;
                font-weight: bold;
                border-left: 3px solid #FF4B4B !important;
            }}
            </style>
        """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("Challenge System")
        st.write(f"Usuário: {usuario['nome']}")
        st.divider()

        menu_items = [
            ("Home", "home", "menu_home"),
            ("Desafios", "desafios", "menu_desafios"),
            ("Votacao", "votacao", "menu_votacao"),
            ("Mini-provas", "mini_provas", "menu_miniprovas"),
            ("Quiz ao Vivo", "quiz_ao_vivo", "menu_quiz_ao_vivo"),
            ("Batalha de Equipes", "batalha_de_equipes", "menu_batalha_de_equipes"),
        ]

        if usuario["tipo_usuario"] == "admin":
            menu_items.append(("Admin", "admin", "menu_admin"))

        for label, pagina, key in menu_items:
            if st.button(label, key=key):
                st.session_state.pagina = pagina
                st.rerun()

        st.divider()
        if st.button("Sair", key="menu_sair"):
            st.session_state.usuario_logado = None
            st.session_state.pagina = "login"
            st.rerun()
