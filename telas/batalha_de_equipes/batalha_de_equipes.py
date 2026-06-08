import streamlit as st

from telas.batalha_de_equipes.times        import tela_batalha_times
from telas.batalha_de_equipes.integrantes  import tela_batalha_integrantes
from telas.batalha_de_equipes.regras       import tela_batalha_regras
from telas.batalha_de_equipes.rodada       import tela_batalha_rodada, tela_batalha_respostas
from telas.batalha_de_equipes.gerenciar_batalhas import tela_batalha_gerenciar


def tela_batalha_de_equipes():

    usuario = st.session_state.usuario_logado
    tipo    = usuario.get("tipo_usuario", "aluno")

    st.title("Batalha de Equipes")
    st.divider()

    # ── Abas de acordo com o perfil ──────────────────────────────────────────
    if tipo == "professor":
        abas = st.tabs([
            "  Times",
            "  Integrantes",
            "  Regras",
            "  Batalhas em Andamento",
            "  Gerenciar Batalhas",
        ])
        tab_times, tab_integrantes, tab_regras, tab_rodada, tab_gerenciar = abas
    else:
        abas = st.tabs([
            "  Times",
            "  Integrantes",
            "  Regras",
            "  Batalhas Abertas",
            "  Minhas Respostas",
        ])
        tab_times, tab_integrantes, tab_regras, tab_rodada, tab_respostas = abas

    # ── Conteúdo de cada aba ─────────────────────────────────────────────────
    with tab_times:
        _render_sem_voltar(tela_batalha_times)

    with tab_integrantes:
        _render_sem_voltar(tela_batalha_integrantes)

    with tab_regras:
        _render_sem_voltar(tela_batalha_regras)

    with tab_rodada:
        _render_sem_voltar(tela_batalha_rodada)

    if tipo == "professor":
        with tab_gerenciar:
            _render_sem_voltar(tela_batalha_gerenciar)
    else:
        with tab_respostas:
            _render_sem_voltar(tela_batalha_respostas)

def _render_sem_voltar(fn):
    """Executa fn() pulando o primeiro botão 'Voltar' que ela renderizar."""

    original_button = st.button
    _chamadas = {"n": 0}

    def botao_filtrado(label, *args, **kwargs):
        if label == "Voltar" and _chamadas["n"] == 0:
            _chamadas["n"] += 1
            # renderiza mas invisível via CSS (não gera clique)
            st.markdown(
                "<style>.btn-voltar-oculto{display:none}</style>",
                unsafe_allow_html=True,
            )
            return False          # nunca clicado
        return original_button(label, *args, **kwargs)

    st.button = botao_filtrado
    try:
        fn()
    finally:
        st.button = original_button
