import streamlit as st


def mostrar_menu():

    with st.sidebar:

        st.title("Challenge System")

        usuario = st.session_state.usuario_logado

        st.write(
            f"Usuário: {usuario['nome']}"
        )

        st.divider()

        if st.button(
            "Home",
            key="menu_home"
        ):

            st.session_state.pagina = "home"

            st.rerun()

        if st.button(
            "Desafios",
            key="menu_desafios"
        ):

            st.session_state.pagina = "desafios"

            st.rerun()

        if st.button(
            "Votação",
            key="menu_votacao"
        ):

            st.session_state.pagina = "votacao"

            st.rerun()

        if st.button(
            "Mini-provas",
            key="menu_miniprovas"
        ):

            st.session_state.pagina = "quiz_ao_vivo"

            st.rerun()

        if st.button(
            "Quiz ao Vivo",
            key="menu_quiz_ao_vivo"
        ):

            st.session_state.pagina = "quiz_ao_vivo"

            st.rerun()
            
        if st.button(
            "Batalha de Equipes",
            key="menu_batalha_de_equipes"
        ):

            st.session_state.pagina = "batalha_de_equipes"

            st.rerun()
    

        if usuario["tipo_usuario"] == "admin":

            if st.button(
                "Admin",
                key="menu_admin"
            ):

                st.session_state.pagina = "admin"

                st.rerun()

        st.divider()

        if st.button(
            "Sair",
            key="menu_sair"
        ):

            st.session_state.usuario_logado = None

            st.session_state.pagina = "login"

            st.rerun()
