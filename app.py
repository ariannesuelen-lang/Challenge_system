import streamlit as st

from utils.session import iniciar_session
from components.navbar import mostrar_menu

from telas.login import tela_login
from telas.cadastro import tela_cadastro
from telas.home import tela_home
from telas.votacao import tela_votacao

# Imports com fallback para telas que podem nao existir ainda
try:
    from telas.desafios import tela_desafios
except ImportError:
    def tela_desafios():
        st.warning("Tela de desafios em desenvolvimento.")

try:
    from telas.voto import tela_voto
except ImportError:
    def tela_voto():
        st.warning("Tela de voto em desenvolvimento.")

try:
    from telas.quiz_ao_vivo import tela_quiz_ao_vivo
except ImportError:
    def tela_quiz_ao_vivo():
        st.warning("Tela de quiz ao vivo em desenvolvimento.")

try:
    from telas.admin import tela_admin
except ImportError:
    def tela_admin():
        st.warning("Tela de admin em desenvolvimento.")

# Mini Provas
try:
    from telas.mini_provas.mini_provas import tela_mini_provas
except ImportError:
    def tela_mini_provas():
        st.warning("Tela de mini provas em desenvolvimento.")

try:
    from telas.mini_provas.mini_provas_professor import tela_mini_provas_professor
except ImportError:
    def tela_mini_provas_professor():
        st.warning("Painel do professor em desenvolvimento.")

try:
    from telas.mini_provas.realizar_mini_prova import tela_realizar_mini_prova
except ImportError:
    def tela_realizar_mini_prova():
        st.warning("Tela em desenvolvimento.")

try:
    from telas.mini_provas.resultados_mini_provas import tela_resultados_mini_provas
except ImportError:
    def tela_resultados_mini_provas():
        st.warning("Tela em desenvolvimento.")

try:
    from telas.mini_provas.resultado_mini_prova import tela_resultado_mini_prova
except ImportError:
    def tela_resultado_mini_prova():
        st.warning("Tela em desenvolvimento.")

try:
    from telas.mini_provas.desempenho_mini_provas import tela_desempenho_mini_provas
except ImportError:
    def tela_desempenho_mini_provas():
        st.warning("Tela em desenvolvimento.")

try:
    from telas.mini_provas.pontuacao_mini_provas import tela_pontuacao_mini_provas
except ImportError:
    def tela_pontuacao_mini_provas():
        st.warning("Tela em desenvolvimento.")

try:
    from telas.mini_provas.cadastro_perguntas import tela_cadastro_perguntas
except ImportError:
    def tela_cadastro_perguntas():
        st.warning("Tela em desenvolvimento.")

try:
    from telas.mini_provas.cadastro_mini_provas import tela_cadastro_mini_provas
except ImportError:
    def tela_cadastro_mini_provas():
        st.warning("Tela em desenvolvimento.")

try:
    from telas.mini_provas.notificacoes_mini_provas import tela_notificacoes_mini_provas
except ImportError:
    def tela_notificacoes_mini_provas():
        st.warning("Tela em desenvolvimento.")

try:
    from telas.mini_provas.solicitacoes_reabertura import tela_solicitacoes_reabertura
except ImportError:
    def tela_solicitacoes_reabertura():
        st.warning("Tela em desenvolvimento.")

try:
    from telas.mini_provas.lista_perguntas import tela_lista_perguntas
except ImportError:
    def tela_lista_perguntas():
        st.warning("Tela em desenvolvimento.")

try:
    from telas.mini_provas.visualizar_mini_prova import tela_visualizar_mini_prova
except ImportError:
    def tela_visualizar_mini_prova():
        st.warning("Tela em desenvolvimento.")

# Batalha de Equipes
try:
    from telas.batalha_de_equipes.batalha_de_equipes import tela_batalha_de_equipes
    from telas.batalha_de_equipes.times import tela_batalha_times
    from telas.batalha_de_equipes.integrantes import tela_batalha_integrantes
    from telas.batalha_de_equipes.gerenciar_batalhas import tela_batalha_gerenciar
    from telas.batalha_de_equipes.rodada import tela_batalha_rodada, tela_batalha_respostas
    from telas.batalha_de_equipes.regras import tela_batalha_regras
except ImportError:
    def tela_batalha_de_equipes():
        st.warning("Modulo de batalha em desenvolvimento.")
    def tela_batalha_times(): pass
    def tela_batalha_integrantes(): pass
    def tela_batalha_gerenciar(): pass
    def tela_batalha_rodada(): pass
    def tela_batalha_respostas(): pass
    def tela_batalha_regras(): pass


# --------------------------------------------------
# CONFIGURACAO
# --------------------------------------------------

st.set_page_config(
    page_title="Challenge System",
    layout="centered"
)

iniciar_session()

# --------------------------------------------------
# AUTENTICACAO
# --------------------------------------------------

if not st.session_state.get("usuario_logado"):
    pagina_auth = st.session_state.get("pagina", "login")
    if pagina_auth == "cadastro":
        tela_cadastro()
    else:
        tela_login()
    st.stop()

# --------------------------------------------------
# MENU
# --------------------------------------------------

mostrar_menu()

# --------------------------------------------------
# ROTEADOR
# --------------------------------------------------

pagina      = st.session_state.get("pagina", "home")
usuario     = st.session_state.get("usuario_logado", {})
tipo_usuario = usuario.get("tipo_usuario", "aluno")

if pagina == "home":
    tela_home()

elif pagina == "desafios":
    tela_desafios()

elif pagina == "votacao":
    tela_votacao()

elif pagina == "voto":
    tela_voto()

elif pagina == "quiz_ao_vivo":
    tela_quiz_ao_vivo()

elif pagina == "admin":
    tela_admin()

# Mini Provas
elif pagina == "mini_provas":
    if tipo_usuario == "professor":
        tela_mini_provas_professor()
    else:
        tela_mini_provas()

elif pagina == "realizar_mini_prova":
    tela_realizar_mini_prova()

elif pagina == "resultados_mini_provas":
    tela_resultados_mini_provas()

elif pagina == "resultado_mini_prova":
    tela_resultado_mini_prova()

elif pagina == "desempenho_mini_provas":
    tela_desempenho_mini_provas()

elif pagina == "pontuacao_mini_provas":
    tela_pontuacao_mini_provas()

elif pagina == "cadastro_perguntas":
    tela_cadastro_perguntas()

elif pagina == "cadastro_mini_provas":
    tela_cadastro_mini_provas()

elif pagina == "notificacoes_mini_provas":
    tela_notificacoes_mini_provas()

elif pagina == "solicitacoes_reabertura":
    tela_solicitacoes_reabertura()

elif pagina == "lista_perguntas":
    tela_lista_perguntas()

elif pagina == "visualizar_mini_prova":
    tela_visualizar_mini_prova()

# Batalha de Equipes
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

else:
    tela_home()
