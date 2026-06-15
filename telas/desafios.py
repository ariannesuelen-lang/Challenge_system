import streamlit as st
from services.desafio_service import listar_desafios, criar_desafio
from utils.estilo import aplicar_estilo, cabecalho

def tela_desafios():
    aplicar_estilo()
    
    usuario = st.session_state.get("usuario_logado", {})
    tipo_usuario = usuario.get("tipo_usuario", "aluno")
    usuario_id = usuario.get("id")

    cabecalho("Central de Desafios", "Explore os desafios de programacao disponiveis ou crie novos.")

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
                titulo = desafio.get('titulo', 'Sem Titulo')
                descricao = desafio.get('descricao', 'Sem descricao.')
                nivel = desafio.get("nivel_dificuldade") or desafio.get("nivel") or "Nao informado"
                prazo = desafio.get('data_limite', 'Sem prazo')

                # Injecao direta de HTML estruturado para forcar o comportamento do CSS customizado
                st.markdown(f"""
                <div style="
                    background-color: #ffffff;
                    border: 1px solid #e0e0e0;
                    border-left: 5px solid #1b3a5c;
                    border-radius: 8px;
                    padding: 20px;
                    margin-bottom: 15px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                ">
                    <h3 style="margin-top: 0; color: #1b3a5c; font-size: 20px;">{titulo}</h3>
                    <p style="color: #333333; font-size: 14px; line-height: 1.5;">{descricao}</p>
                    <div style="display: flex; justify-content: space-between; margin-top: 15px; border-top: 1px solid #f0f0f0; padding-top: 10px;">
                        <span style="font-size: 12px; color: #666666;"><strong>Nivel:</strong> {nivel}</span>
                        <span style="font-size: 12px; color: #666666;"><strong>Prazo:</strong> {prazo}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

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
