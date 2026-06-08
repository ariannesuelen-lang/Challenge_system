import streamlit as st
from services.votacao_service import listar_votos, registrar_voto
from services.desafio_service import listar_desafios
from utils.estilo import aplicar_estilo, cabecalho  # Importações do seu CSS global


def tela_votacao():
    # Aplica o CSS padrão do sistema
    aplicar_estilo()

    usuario = st.session_state.get("usuario_logado", {})
    desafios = listar_desafios()

    cabecalho(
        "Sistema de Votacao",
        "Vote nos melhores projetos ou gerencie as votacoes ativas"
    )

    tipo = usuario.get("tipo_usuario", "aluno")

    if tipo == "professor":
        st.subheader("Gerenciamento de Votos")
        
        if st.button("Listar Todos os Votos", width="stretch"):
            votos = listar_votos()
            if votos:
                for v in votos:
                    # Card estilizado simulando o padrão do sistema
                    st.markdown(f"""
                    <div style="
                        background: #f0f9ff;
                        border-left: 4px solid #1b3a5c;
                        border-radius: 8px;
                        padding: 12px 16px;
                        margin-bottom: 8px;
                    ">
                        <span style="color: #0d1b2a; font-weight: 600;">Desafio ID: {v.get('desafio_id')}</span><br>
                        <span style="color: #555; font-size: 13px;">Aluno ID: {v.get('aluno_id')} | Votos: {v.get('votos', 0)}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Nenhum voto registrado ate o momento.")
    else:
        st.subheader("Escolha um Desafio para Votar")
        
        if desafios:
            # Criando uma lista limpa para o selectbox
            opcoes_desafios = {d['titulo']: d['id'] for d in desafios}
            escolha_titulo = st.selectbox("Selecione o desafio:", list(opcoes_desafios.keys()))
            desafio_id = opcoes_desafios[escolha_titulo]

            aluno_id = st.number_input("ID do Aluno Autor do Projeto", min_value=1, step=1)

            if st.button("Confirmar Voto", width="stretch"):
                if aluno_id == usuario.get("id"):
                    st.error("Voce nao pode votar no seu proprio projeto.")
                else:
                    resultado = registrar_voto(desafio_id, aluno_id)
                    if resultado.get("sucesso"):
                        st.success("Seu voto foi registrado com sucesso!")
                    else:
                        st.error(resultado.get("mensagem", "Erro ao registrar voto."))
        else:
            st.info("Nenhum desafio disponivel para votacao no momento.")
