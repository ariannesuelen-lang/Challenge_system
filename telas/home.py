import streamlit as st
from services.desafio_service import listar_desafios
from utils.estilo import aplicar_estilo, cabecalho

def tela_home():
    aplicar_estilo()
    
    usuario = st.session_state.get("usuario_logado", {})
    nome_usuario = usuario.get("nome", "Usuário")
    
    cabecalho(
        f"Olá, {nome_usuario}!",
        "Bem-vindo ao Challenge System."
    )
    
    st.subheader("Desafios em Destaque")
    
    try:
        desafios = listar_desafios()
    except Exception:
        desafios = []
        
    if not desafios:
        st.info("Nenhum desafio localizado.")
        return

    for desafio in desafios[:3]:
        with st.container(border=True):
            st.markdown(f"### {desafio.get('titulo', 'Sem Título')}")
            st.write(desafio.get("descricao", "Sem descrição disponível."))
            
            col1, col2 = st.columns(2)
            with col1:
                # Fallback em cadeia para garantir compatibilidade com o dicionário
                nivel = desafio.get("nivel_dificuldade") or desafio.get("nivel") or "Não informado"
                st.caption(f"**Nível:** {nivel}")
            with col2:
                prazo = desafio.get("data_limite", "Sem prazo")
                st.caption(f"**Prazo final:** {prazo}")
