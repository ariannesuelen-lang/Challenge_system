import streamlit as st

from utils.session import iniciar_session

from components.navbar import mostrar_menu
from telas.login import tela_login
from telas.cadastro import tela_cadastro
from telas.home import tela_home
from telas.quiz_ao_vivo import tela_quiz_ao_vivo
from telas.batalha_de_equipes import tela_batalha_de_equipes
from telas.votacao import tela_votacao
from telas.voto import tela_voto
from telas.desafios import tela_desafios

from telas.mini_provas.mini_provas import (
    tela_mini_provas
)

from telas.mini_provas.mini_provas_professor import (
    tela_mini_provas_professor
)

from telas.mini_provas.realizar_mini_prova import (
    tela_realizar_mini_prova
)

from telas.mini_provas.resultados_mini_provas import (
    tela_resultados_mini_provas
)

from telas.mini_provas.resultado_mini_prova import (
    tela_resultado_mini_prova
)

from telas.mini_provas.desempenho_mini_provas import (
    tela_desempenho_mini_provas
)

from telas.mini_provas.pontuacao_mini_provas import (
    tela_pontuacao_mini_provas
)

from telas.mini_provas.cadastro_perguntas import (
    tela_cadastro_perguntas
)

from telas.mini_provas.cadastro_mini_provas import (
    tela_cadastro_mini_provas
)

from telas.mini_provas.notificacoes_mini_provas import (
    tela_notificacoes_mini_provas
)

from telas.mini_provas.solicitacoes_reabertura import (
    tela_solicitacoes_reabertura
)


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

elif st.session_state.pagina == "voto":
    tela_voto()
    
elif st.session_state.pagina == "quiz_ao_vivo":
    tela_quiz_ao_vivo()

elif st.session_state.pagina == "batalha_de_equipes":
    tela_batalha_de_equipes()

elif st.session_state.pagina == "mini_provas":

    if st.session_state.tipo_usuario == "professor":

        tela_mini_provas_professor()

    else:

        tela_mini_provas()

elif st.session_state.pagina == "pontuacao_mini_provas":

    tela_pontuacao_mini_provas()

elif st.session_state.pagina == "resultados_mini_provas":

    tela_resultados_mini_provas()

elif st.session_state.pagina == "realizar_mini_prova":

    tela_realizar_mini_prova()

elif st.session_state.pagina == "cadastro_perguntas":

    tela_cadastro_perguntas()

elif st.session_state.pagina == "cadastro_mini_provas":

    tela_cadastro_mini_provas()

elif st.session_state.pagina == "solicitacoes_reabertura":

    tela_solicitacoes_reabertura()
