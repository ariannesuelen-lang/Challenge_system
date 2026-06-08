import streamlit as st
from utils.session import iniciar_session
from telas.login import tela_login
from telas.cadastro import tela_cadastro
from telas.home import tela_home
from telas.votacao import tela_votacao

# TENTATIVA RESILIENTE DE IMPORTAÇÃO DA NAVBAR
try:
    from components.navbar import mostrar_menu
except ImportError:
    try:
        from components.navbar import navbar as mostrar_menu
    except ImportError:
        try:
            from components.navbar import criar_navbar as mostrar_menu
        except ImportError:
            # Caso a função não mude de nome, gera um menu básico em HTML para não travar o boot
            def mostrar_menu():
                st.sidebar.title("Menu do Sistema")
                return st.sidebar.radio("Navegação", ["Home", "Votação"])

# Fallbacks dinâmicos para outras telas caso não existam no repositório
try: from telas.desafios import tela_desafios
except ImportError: def tela_desafios(): st.warning("Tela em desenvolvimento.")

try: from telas.mini_provas.mini_provas_professor import tela_mini_provas_professor
except ImportError: def tela_mini_provas_professor(): st.warning("Tela em desenvolvimento.")

try: from telas.mini_provas.mini_provas_aluno import tela_mini_provas as tela_mini_provas_aluno
except ImportError: def tela_mini_provas_aluno(): st.warning("Tela em desenvolvimento.")


def main():
    # Inicializa as variáveis necessárias de sessão
    iniciar_session()
    
    # Se o usuário não estiver autenticado, força a tela de Login ou Cadastro
    if not st.session_state.get("usuario_logado"):
        pagina_auth = st.session_state.get("pagina", "login")
        if pagina_auth == "cadastro":
            tela_cadastro()
        else:
            tela_login()
        return

    # Usuário autenticado: Carrega o menu de navegação lateral ou superior
    mostrar_menu()
    
    # Roteador de Páginas baseado no state do app
    pagina = st.session_state.get("pagina", "home")
    usuario = st.session_state.get("usuario_logado", {})
    tipo_usuario = usuario.get("tipo_usuario", "aluno")

    if pagina == "home":
        tela_home()
    elif pagina == "desafios":
        tela_desafios()
    elif pagina == "votacao":
        tela_votacao()
    elif pagina == "mini_provas":
        if tipo_usuario == "professor":
            tela_mini_provas_professor()
        else:
            tela_mini_provas_aluno()
            
if __name__ == "__main__":
    main()
