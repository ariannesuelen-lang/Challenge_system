import streamlit as st


def mostrar_menu():
    pagina_atual = st.session_state.get("pagina", "home")
    usuario      = st.session_state.usuario_logado

    # CSS injetado ANTES do with st.sidebar para garantir precedência
    st.markdown("""
        <style>
        /* Botoes da sidebar: base transparente */
        [data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            text-align: left !important;
            background-color: transparent !important;
            border: none !important;
            color: #ffffff !important;
            padding: 0.5rem 1rem !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: background 0.2s !important;
            box-shadow: none !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: #00b4d8 !important;
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] .stButton > button:focus,
        [data-testid="stSidebar"] .stButton > button:active {
            background-color: transparent !important;
            box-shadow: none !important;
        }
        /* Botao ativo: ciano com borda esquerda branca */
        [data-testid="stSidebar"] .botao-ativo .stButton > button {
            background-color: #00b4d8 !important;
            color: #ffffff !important;
            border-left: 4px solid #ffffff !important;
            padding-left: 0.85rem !important;
            font-size: 1.02rem !important;
        }
        [data-testid="stSidebar"] .botao-ativo .stButton > button:focus,
        [data-testid="stSidebar"] .botao-ativo .stButton > button:active {
            background-color: #00b4d8 !important;
            box-shadow: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    menu_items = [
        ("Home",               "home",               "menu_home"),
        ("Desafios",           "desafios",            "menu_desafios"),
        ("Votação",            "votacao",             "menu_votacao"),
        ("Mini-provas",        "mini_provas",         "menu_miniprovas"),
        ("Quiz ao Vivo",       "quiz_ao_vivo",        "menu_quiz_ao_vivo"),
        ("Batalha de Equipes", "batalha_de_equipes",  "menu_batalha_de_equipes"),
    ]

    if usuario["tipo_usuario"] == "admin":
        menu_items.append(("Admin", "admin", "menu_admin"))

    with st.sidebar:
        st.title("Challenge System")
        st.write(f"Usuário: {usuario['nome']}")
        st.divider()

        for label, pagina, key in menu_items:
            ativo = pagina_atual == pagina
            if ativo:
                st.markdown('<div class="botao-ativo">', unsafe_allow_html=True)
            if st.button(label, key=key):
                st.session_state.pagina = pagina
                st.rerun()
            if ativo:
                st.markdown('</div>', unsafe_allow_html=True)

        st.divider()
        if st.button("Sair", key="menu_sair"):
            st.session_state.usuario_logado = None
            st.session_state.pagina = "login"
            st.rerun()
