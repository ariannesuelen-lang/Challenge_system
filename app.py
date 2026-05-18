import streamlit as st

from utils.session import iniciar_session

from components.navbar import mostrar_menu

from pages.telas.login import tela_login
from pages.telas.cadastro import tela_cadastro
from pages.telas.home import tela_home
from pages.telas.quiz_ao_vivo import tela_quiz_ao_vivo
from pages.telas.batalha_de_equipes import tela_batalha_de_equipes

from pages.telas.mini_provas import tela_mini_provas
from pages.telas.votacao import tela_votacao

from pages.telas.desafios import tela_desafios

st.set_page_config(
    page_title="Challenge System",
    layout="centered"
)

iniciar_session()

pagina = st.session_state.pagina

if st.session_state.usuario_logado:

    mostrar_menu()

if pagina == "login":

    tela_login()

elif pagina == "cadastro":

    tela_cadastro()

elif pagina == "home":

    if not st.session_state.usuario_logado:

        st.session_state.pagina = "login"

        st.rerun()

    tela_home()

elif st.session_state.pagina == "desafios":
    tela_desafios()

elif st.session_state.pagina == "votacao":
    tela_votacao()

elif st.session_state.pagina == "mini_provas":
    tela_mini_provas()

elif st.session_state.pagina == "quiz_ao_vivo":
    quiz_ao_vivo()

elif st.session_state.pagina == "batalha_de_equipes":
    batalha_de_equipes()
