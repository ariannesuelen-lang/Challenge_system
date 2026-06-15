import streamlit as st
from datetime import date

from services import batalha_service 
from utils.estilo import aplicar_estilo, cabecalho


def tela_batalha_gerenciar():
    aplicar_estilo()

    usuario = st.session_state.usuario_logado
    tipo    = usuario.get(\"tipo_usuario\", \"aluno\")
    user_id = usuario.get(\"id\")

    if tipo not in (\"professor\", \"admin\"):
        st.error(\"Acesso restrito a professores.\")
        return

    cabecalho(\"Gerenciar Batalhas\", \"Crie e controle as batalhas de equipes\")

    if st.button(\"Voltar\"):
        st.session_state.pagina = \"batalha_de_equipes\"
        st.rerun()

    st.divider()
    st.markdown(\"### Nova Batalha\")

    with st.container(border=True):
        titulo    = st.text_input(\"Titulo da batalha\", placeholder=\"Ex: Batalha de Algoritmos\")
        descricao = st.text_area(\"Descricao / objetivo\", placeholder=\"Descreva o objetivo da batalha\")

        col1, col2 = st.columns(2)
        with col1:
            quantidade_rodadas = st.number_input(\"Numero de rodadas\", min_value=1, value=1)
            
        # EXEMPLO DE CHAMADA 1: Listando batalhas usando o novo objeto
        batalhas = batalha_service.listar_batalhas()
        abertas  = [b for b in batalhas if not b.get(\"finalizada\")]

        # ... resto do seu formulário visual do Streamlit ...
        
        if st.button(\"Criar Batalha\", use_container_width=True):
            # EXEMPLO DE CHAMADA 2: Criando batalha através do método da classe
            sucesso = batalha_service.criar_batalha(
                titulo=titulo, 
                descricao=descricao, 
                criador_id=user_id, 
                quantidade_rodadas=quantidade_rodadas
            )
            if sucesso:
                st.success(\"Batalha criada!\")
                st.rerun()

    # ... bloco de listagem de batalhas na tela ...
    # Quando o professor clicar para encerrar a batalha no seu laço:
    if st.button(\"Finalizar batalha\", key=f\"fin_{b.get('id')}\"):
        # EXEMPLO DE CHAMADA 3: Finalizando a batalha mapeada
        if batalha_service.finalizar_batalha(b.get('id')):
            st.success(\"Batalha finalizada!\")
            st.rerun()