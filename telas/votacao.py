# telas/votacao.py
import streamlit as st
from services import desafio_service, votacao_service
from utils.estilo import aplicar_estilo, cabecalho

def tela_votacao():
    aplicar_estilo()

    usuario = st.session_state.get("usuario_logado", {})
    tipo = usuario.get("tipo_usuario", "aluno")
    usuario_id_logado = str(usuario.get("id", ""))

    cabecalho(
        "Sistema de Votação",
        "Vote nos melhores projetos ou gerencie as votações ativas"
    )

    if tipo == "professor":
        st.subheader("Gerenciamento de Votos")
        
        if st.button("Listar Todos os Votos", use_container_width=True):
            # 🌟 ALTERADO: Consumo da lista de votos unificada pela Service
            votos = votacao_service.listar_votos()
            if votos:
                for v in votos:
                    st.markdown(f"""
                    <div style="
                        background: #f0f9ff;
                        border-left: 4px solid #1b3a5c;
                        border-radius: 8px;
                        padding: 12px 16px;
                        margin-bottom: 8px;
                    ">
                        <span style="color: #0d1b2a; font-weight: 600;">Desafio ID: {v.get('desafio_id', '-')}</span><br>
                        <span style="color: #555; font-size: 13px;">Eleitor (ID): {v.get('usuario_id', '-')} | Votou no Aluno (ID): {v.get('voto', '-')}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Nenhum voto registrado até o momento.")
                
    else:
        st.subheader("Pesquisar e Votar")
        pesquisa = st.text_input("Pesquisar desafio por título")
        
        desafios = desafio_service.listar_desafios()

        if pesquisa and desafios:
            desafios = [d for d in desafios if pesquisa.lower() in d.get("titulo", "").lower()]

        if not desafios:
            st.warning("Nenhum desafio ativo encontrado para votação no momento.")
            
            # Bloco de redundância para votação manual caso a listagem geral esteja vazia
            with st.container(border=True):
                st.caption("Votação Manual (Insira os IDs manualmente)")
                desafio_id_manual = st.number_input("ID do Desafio", min_value=1, step=1, key="manual_desafio_id")
                aluno_id = st.number_input("ID do Aluno Autor do Projeto", min_value=1, step=1, key="manual_aluno_id")
                
                if st.button("Confirmar Voto", key="voto_manual_btn", use_container_width=True):
                    if str(aluno_id) == usuario_id_logado:
                        st.error("Você não pode votar no seu próprio projeto.")
                    else:
                        _processar_voto(str(desafio_id_manual), str(aluno_id), usuario_id_logado)
        else:
            for desafio in desafios:
                with st.container(border=True):
                    st.subheader(desafio.get("titulo", "Sem Título"))
                    st.write(f"Prazo final: {desafio.get('data_limite', 'Não informado')}")
                    
                    aluno_id = st.number_input(
                        "ID do Aluno Autor do Projeto", 
                        min_value=1, 
                        step=1, 
                        key=f"aluno_id_{desafio.get('id')}"
                    )

                    if st.button("Confirmar Voto", key=f"voto_{desafio.get('id')}", use_container_width=True):
                        if str(aluno_id) == usuario_id_logado:
                            st.error("Você não pode votar no seu próprio projeto.")
                        else:
                            _processar_voto(str(desafio.get('id')), str(aluno_id), usuario_id_logado)


def _processar_voto(desafio_id, aluno_id, usuario_id_logado):
    # 🌟 ALTERADO: Gravação acionada via inteligência do monólito
    resultado = votacao_service.registrar_voto(desafio_id, aluno_id, usuario_id_logado)
    
    if resultado.get("sucesso"):
        st.success(resultado.get("mensagem"))
        st.rerun()
    else:
        st.error(resultado.get("mensagem", "Erro ao registrar voto."))