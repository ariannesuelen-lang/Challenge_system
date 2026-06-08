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
        [data-testid="stSidebar"] .botao-ativo .stButton > button {
            background-color: rgba(255,75,75,0.2) !important;
            font-weight: bold;
            border-left: 3px solid #FF4B4B !important;
            color: #FF4B4B !important;
        }
        </style>
    """, unsafe_allow_html=True)

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
