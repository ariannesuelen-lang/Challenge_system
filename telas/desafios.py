import streamlit as st
from services.desafio_service import listar_desafios, criar_desafio
from utils.estilo import aplicar_estilo, cabecalho

def tela_desafios():
    aplicar_estilo()
    
    usuario = st.session_state.get("usuario_logado", {})
    tipo_usuario = usuario.get("tipo_usuario", "aluno")
    usuario_id = usuario.get("id")

    cabecalho("Central de Desafios", "Explore os desafios de programacao disponiveis ou crie novos.")

    # Define o layout em abas com base no perfil do usuario conectado
    if tipo_usuario == "professor":
        aba1, aba2 = st.tabs(["Desafios Ativos", "Criar Novo Desafio"])
    else:
        aba1, = st.tabs(["Desafios Ativos"])

    with aba1:
        st.subheader("Lista de Desafios")
        try:
            desafios = listar_desafios()
        except Exception:
            desafios = []

        if not desafios:
            st.info("Nenhum desafio disponivel no momento.")
        else:
            for desafio in desafios:
                with st.container(border=True):
                    st.markdown(f"### {desafio.get('titulo', 'Sem Titulo')}")
                    st.write(desafio.get("descricao", "Sem descricao."))
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        nivel = desafio.get("nivel_dificuldade") or desafio.get("nivel") or "Nao informado"
                        st.caption(f"**Nivel:** {nivel}")
                    with col2:
                        st.caption(f"**Prazo:** {desafio.get('data_limite', 'Sem prazo')}")

    if tipo_usuario == "professor":
        with aba2:
            st.subheader("Cadastrar Novo Desafio")
            with st.form("form_novo_desafio"):
                titulo = st.text_input("Titulo do Desafio")
                descricao = st.text_area("Descricao / Enunciado")
                nivel = st.selectbox("Nivel de Dificuldade", ["Facil", "Medio", "Dificil"])
                data_limite = st.date_input("Data Limite (Opcional)", value=None)
                
                enviado = st.form_submit_button("Salvar Desafio", width="stretch")
                if enviado:
                    if not titulo or not descricao:
                        st.error("Por favor, preencha o titulo e a descricao.")
                    else:
                        res = criar_desafio(titulo, descricao, usuario_id, data_limite, nivel)
                        if res.get("sucesso"):
                            st.success("Desafio criado com sucesso!")
                            st.rerun()
                        else:
                            st.error(res.get("mensagem", "Erro ao criar desafio."))
