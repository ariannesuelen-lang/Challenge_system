import streamlit as st

from utils.session import iniciar_session

from components.navbar import mostrar_menu
from telas.login import tela_login
from telas.cadastro import tela_cadastro
from telas.home import tela_home

# Importacao direta usando o nome exato do arquivo no seu GitHub
from telas.quiz_ao_vivo import tela_quiz_ao_vivo

from telas.votacao import tela_votacao
from telas.voto import tela_voto
from telas.desafios import tela_desafios

from telas.mini_provas.mini_provas import tela_mini_provas
from telas.mini_provas.mini_provas_professor import tela_mini_provas_professor
from telas.mini_provas.realizar_mini_prova import tela_realizar_mini_prova
from telas.mini_provas.resultados_mini_provas import tela_resultados_mini_provas
from telas.mini_provas.resultado_mini_prova import tela_resultado_mini_prova
from telas.mini_provas.desempenho_mini_provas import tela_desempenho_mini_provas
from telas.mini_provas.pontuacao_mini_provas import tela_pontuacao_mini_provas
from telas.mini_provas.cadastro_perguntas import tela_cadastro_perguntas
from telas.mini_provas.cadastro_mini_provas import tela_cadastro_mini_provas
from telas.mini_provas.notificacoes_mini_provas import tela_notificacoes_mini_provas
from telas.mini_provas.solicitacoes_reabertura import tela_solicitacoes_reabertura
from telas.mini_provas.lista_perguntas import tela_lista_perguntas

from telas.batalha_de_equipes.batalha_de_equipes import tela_batalha_de_equipes
from telas.batalha_de_equipes.times import tela_batalha_times
from telas.batalha_de_equipes.integrantes import tela_batalha_integrantes
from telas.batalha_de_equipes.gerenciar_batalhas import tela_batalha_gerenciar
from telas.batalha_de_equipes.rodada import tela_batalha_rodada, tela_batalha_respostas
from telas.batalha_de_equipes.regras import tela_batalha_regras


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

elif pagina == "desafios":
    tela_desafios()

elif pagina == "votacao":
    tela_votacao()

elif pagina == "voto":
    tela_voto()

elif pagina == "quiz_ao_vivo":
    tela_quiz_ao_vivo()

elif pagina == "mini_provas":
    if (
        st.session_state.usuario_logado[
            "tipo_usuario"
        ] == "professor"
    ):
        tela_mini_provas_professor()
    else:
        tela_mini_provas()

elif pagina == "pontuacao_mini_provas":
    tela_pontuacao_mini_provas()

elif pagina == "resultados_mini_provas":
    tela_resultados_mini_provas()

elif pagina == "realizar_mini_prova":
    tela_realizar_mini_prova()

elif pagina == "cadastro_perguntas":
    tela_cadastro_perguntas()

elif pagina == "cadastro_mini_provas":
    tela_cadastro_mini_provas()

elif pagina == "solicitacoes_reabertura":
    tela_solicitacoes_reabertura()

elif pagina == "lista_perguntas":
    tela_lista_perguntas()

elif pagina == "batalha_de_equipes":
    tela_batalha_de_equipes()

elif pagina == "batalha_times":
    tela_batalha_times()

elif pagina == "batalha_integrantes":
    tela_batalha_integrantes()

elif pagina == "batalha_gerenciar":
    tela_batalha_gerenciar()

elif pagina == "batalha_rodada":
    tela_batalha_rodada()

elif pagina == "batalha_respostas":
    tela_batalha_respostas()

elif pagina == "batalha_regras":
    tela_batalha_regras()
