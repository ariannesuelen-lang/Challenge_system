import streamlit as st


def mostrar_menu():

    with st.sidebar:

        st.markdown("""
        <div style="
            background: linear-gradient(180deg, #0d1b2a, #1b3a5c);
            border-radius: 10px;
            padding: 20px 16px 14px;
            margin-bottom: 16px;
            border-bottom: 3px solid #00b4d8;
        ">
            <h2 style="color:#ffffff; margin:0; font-size:20px; letter-spacing:1px;">
                Challenge System
            </h2>
            <p style="color:#90caf9; margin:4px 0 0; font-size:12px;">
                Plataforma de Aprendizado
            </p>
        </div>
        """, unsafe_allow_html=True)

        usuario = st.session_state.usuario_logado

        st.markdown(f"""
        <div style="
            background:#1b3a5c;
            border-radius: 8px;
            padding: 10px 14px;
            margin-bottom: 16px;
            border-left: 3px solid #00b4d8;
        ">
            <p style="color:#90caf9; margin:0; font-size:11px;">Logado como</p>
            <p style="color:#ffffff; margin:2px 0; font-weight:700; font-size:14px;">
                {usuario['nome']}
            </p>
            <p style="
                color:#00b4d8;
                margin:0;
                font-size:11px;
                font-weight:600;
                text-transform:uppercase;
                letter-spacing:1px;
            ">
                {usuario.get('tipo_usuario','aluno').capitalize()}
            </p>
        </div>
        """, unsafe_allow_html=True)

        PAGINAS = [
            ("Home",               "home"),
            ("Desafios",           "desafios"),
            ("Votacao",            "votacao"),
            ("Mini-provas",        "mini_provas"),
            ("Quiz ao Vivo",       "quiz_ao_vivo"),
            ("Batalha de Equipes", "batalha_de_equipes"),
        ]

        pagina_atual = st.session_state.pagina

        for label, pagina in PAGINAS:
            ativo = pagina_atual == pagina or pagina_atual.startswith(pagina)
            if ativo:
                st.markdown(f"""
                <div style="
                    background:#00b4d8;
                    border-radius:6px;
                    padding:8px 12px;
                    margin-bottom:4px;
                    font-weight:700;
                    color:#ffffff;
                    cursor:pointer;
                ">{label}</div>
                """, unsafe_allow_html=True)
                st.button(label, key=f"menu_{pagina}", use_container_width=True,
                          disabled=False, on_click=lambda p=pagina: _ir(p))
            else:
                if st.button(label, key=f"menu_{pagina}", use_container_width=True):
                    st.session_state.pagina = pagina
                    st.rerun()

        if usuario.get("tipo_usuario") == "admin":
            if st.button("Admin", key="menu_admin", use_container_width=True):
                st.session_state.pagina = "admin"
                st.rerun()

        st.divider()

        if st.button("Sair", key="menu_sair", use_container_width=True):
            try:
                st.query_params.clear()
            except Exception:
                pass
            st.session_state.usuario_logado = None
            st.session_state.pagina         = "login"
            st.rerun()


def _ir(pagina):
    st.session_state.pagina = pagina
    st.rerun()
