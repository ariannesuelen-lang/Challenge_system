import streamlit as st
from services.auth_service import login_usuario
from utils.estilo import aplicar_estilo


def tela_login():

    aplicar_estilo()

    col_esq, col_centro, col_dir = st.columns([1, 2, 1])

    with col_centro:

        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #0d1b2a, #1b3a5c);
            border-radius: 16px;
            padding: 36px 32px 28px;
            margin-top: 40px;
            border-top: 4px solid #00b4d8;
            box-shadow: 0 4px 20px rgba(0,180,216,0.15);
        ">
            <h1 style="
                color:#ffffff;
                text-align:center;
                margin:0 0 6px;
                font-size:28px;
                letter-spacing:1px;
            ">Challenge System</h1>
            <p style="
                color:#90caf9;
                text-align:center;
                margin:0 0 28px;
                font-size:14px;
            ">Plataforma de Aprendizado</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <h3 style="color:#0d1b2a; margin-bottom:16px;">Entrar na conta</h3>
        """, unsafe_allow_html=True)

        with st.form("form_login"):

            email = st.text_input("E-mail", placeholder="seu@email.com")
            senha = st.text_input("Senha", type="password", placeholder="••••••••")

            st.markdown("<br>", unsafe_allow_html=True)
            entrar = st.form_submit_button("Entrar", use_container_width=True)

        if entrar:
            if not email or not senha:
                st.warning("Preencha todos os campos.")
            else:
                usuario = login_usuario(email, senha)
                if usuario:
                    st.session_state.usuario_logado = usuario
                    st.session_state.pagina         = "home"
                    try:
                        st.query_params["uid"] = str(usuario.get("id", ""))
                    except Exception:
                        pass
                    st.rerun()
                else:
                    st.error("E-mail ou senha invalidos.")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Criar conta", use_container_width=True):
                st.session_state.pagina = "cadastro"
                st.rerun()
