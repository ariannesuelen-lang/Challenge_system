# app.py
import streamlit as st

# Inicialização e Componentes Globais
from utils.session import iniciar_session
from components.navbar import mostrar_menu

# Telas Centrais da Raiz de Telas
from telas.login import tela_login
from telas.cadastro import tela_cadastro
from telas.home import tela_home
from telas.votacao import tela_votacao
from telas.desafios import tela_desafios
from telas.quiz_ao_vivo import tela_quiz_ao_vivo
from telas.admin import tela_admin

# Importações Limpas via Pacotes __init__.py das Subpastas
from telas.mini_provas import tela_mini_provas, tela_mini_provas_professor
from telas.mini_provas.realizar_mini_prova import tela_realizar_mini_prova
from telas.mini_provas.historico_provas import tela_historico_provas       # 📊 Arquivo Renomeado!
from telas.mini_provas.resultado_mini_prova import tela_resultado_mini_prova
from telas.mini_provas.desempenho_mini_provas import tela_desempenho_mini_provas
from telas.mini_provas.pontuacao_mini_provas import tela_pontuacao_mini_provas
from telas.mini_provas.cadastro_perguntas import tela_cadastro_perguntas
from telas.mini_provas.cadastro_mini_provas import tela_cadastro_mini_provas
from telas.mini_provas.solicitacoes_reabertura import tela_solicitacoes_reabertura
from telas.mini_provas.lista_perguntas import tela_lista_perguntas
from telas.mini_provas.visualizar_mini_prova import tela_visualizar_mini_prova

from telas.batalha_de_equipes import tela_batalha_de_equipes               # ⚔️ Importação curta via __init__.py


# --------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA STREAMLIT
# --------------------------------------------------
st.set_page_config(
    page_title="Challenge System",
    layout="centered"
)

# Inicializa o controle global da sessão
iniciar_session()


# --------------------------------------------------
# FLUXO FORÇADO DE AUTENTICAÇÃO
# --------------------------------------------------
if not st.session_state.get("usuario_logado"):
    pagina_auth = st.session_state.get("pagina", "login")
    if pagina_auth == "cadastro":
        tela_cadastro()
    else:
        tela_login()
    st.stop()


# --------------------------------------------------
# RENDERIZAÇÃO DO MENU LATERAL (SIDEBAR)
# --------------------------------------------------
mostrar_menu()


# --------------------------------------------------
# ROTEADOR CENTRAL DE PÁGINAS (STATE MACHINE)
# --------------------------------------------------
pagina       = st.session_state.get("pagina", "home")
usuario      = st.session_state.get("usuario_logado", {})
tipo_usuario = usuario.get("tipo_usuario", "aluno")

# 🏠 Módulo Geral e de Votações
if pagina == "home":
    tela_home()

elif pagina == "desafios":
    tela_desafios()

elif pagina == "votacao":
    tela_votacao()

elif pagina == "quiz_ao_vivo":
    tela_quiz_ao_vivo()

elif pagina == "admin":
    tela_admin()

# 📝 Módulo: Mini Provas (Rotas de Aluno, Professor e Administrativo)
elif pagina == "mini_provas":
    if tipo_usuario == "professor":
        tela_mini_provas_professor()
    else:
        tela_mini_provas()

elif pagina == "realizar_mini_prova":
    tela_realizar_mini_prova()

elif pagina == "historico_provas":                 # 🌟 Rota atualizada com o nome coerente
    tela_historico_provas()

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

elif pagina == "solicitacoes_reabertura":
    tela_solicitacoes_reabertura()

elif pagina == "lista_perguntas":
    tela_lista_perguntas()

elif pagina == "visualizar_mini_prova":
    tela_visualizar_mini_prova()

# ⚔️ Módulo: Batalha de Equipes (Controlado internamente via st.tabs)
elif pagina == "batalha_de_equipes":
    tela_batalha_de_equipes()

# Fallback de segurança para páginas inexistentes ou corrompidas
else:
    tela_home()