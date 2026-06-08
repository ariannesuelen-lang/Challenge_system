import streamlit as st
from utils.estilo import aplicar_estilo, cabecalho

# Fallback seguro para o serviço caso mude de diretório
try:
    from services.mini_provas_service import listar_mini_provas_professor
except ImportError:
    def listar_mini_provas_professor(*args, **kwargs): return []

def tela_mini_provas_professor():
    aplicar_estilo()
    
    cabecalho(
        "Gerenciamento de Mini Provas",
        "Crie, edite e acompanhe o desempenho das avaliações rápidas."
    )
    
    st.subheader("Suas Provas Cadastradas")
    
    usuario = st.session_state.get("usuario_logado", {})
    professor_id = usuario.get("id")
    
    try:
        provas = listar_mini_provas_professor(professor_id)
    except Exception:
        provas = []
        
    if not provas:
        st.info("Você ainda não criou nenhuma mini prova.")
        return
        
    for prova in provas:
        with st.container(border=True):
            st.markdown(f"### {prova.get('titulo', 'Prova Sem Título')}")
            st.write(prova.get("descricao", "Sem descrição definida."))
            
            # CORREÇÃO CRÍTICA: chave alterada de 'qtde_questoes' para 'quantidade_questoes'
            qtd = prova.get("quantidade_questoes") or prova.get("qtde_questoes") or 0
            duracao = prova.get("duracao_minutos") or prova.get("duracao") or 0
            
            st.write(f"**Configuração:** {qtd} questões | Tempo: {duracao} minutos")
            
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"Status: *{prova.get('status', 'rascunho').upper()}*")
            with col2:
                if st.button("Ver Resultados", key=f"res_{prova.get('id')}", width="stretch"):
                    st.session_state.prova_selecionada = prova.get("id")
                    st.info("Carregando relatório...")
