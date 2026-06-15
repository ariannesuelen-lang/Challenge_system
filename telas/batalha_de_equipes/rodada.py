import streamlit as st
from services import batalha_service
from utils.estilo import aplicar_estilo, cabecalho


def tela_batalha_rodada():

    aplicar_estilo()

    usuario = st.session_state.usuario_logado
    tipo    = usuario.get("tipo_usuario", "aluno")
    user_id = usuario.get("id")

    cabecalho("Batalhas em Andamento", "Participe das batalhas abertas")

    if st.button("Voltar"):
        st.session_state.pagina = "batalha_de_equipes"
        st.rerun()

    st.divider()

    # ALTERADO: Chamada utilizando o método do serviço global
    batalhas = batalha_service.listar_batalhas()
    abertas  = [b for b in batalhas if not b.get("finalizada")]

    if not abertas:
        st.markdown("""
        <div style="
            background:#f0f9ff;
            border-left:4px solid #0d1b2a;
            border-radius:8px;
            padding:14px 18px;
        ">
            <span style="color:#0d1b2a; font-weight:600;">Nenhuma batalha aberta no momento.</span>
        </div>
        """, unsafe_allow_html=True)
        return

    mapa_b = {b.get("titulo"): b.get("id") for b in abertas if b.get("titulo")}
    sel_b  = st.selectbox("Escolha uma batalha ativa", list(mapa_b.keys()))
    bid    = mapa_b[sel_b]

    # ALTERADO: Obtendo os detalhes específicos da batalha selecionada
    b_atual = batalha_service.obter_batalha(bid)
    if not b_atual:
        st.error("Erro ao carregar dados da batalha.")
        return

    st.markdown(f"### {b_atual.get('titulo')}")
    if b_atual.get("descricao"):
        st.write(b_atual["descricao"])

    # --------------------------------------------------
    # FLUXO DO ALUNO (SUBMISSÃO DE RESPOSTAS)
    # --------------------------------------------------
    if tipo == "aluno":
        # ALTERADO: Verificação de segurança via classe para checar duplicidade
        if batalha_service.usuario_ja_respondeu(bid, user_id):
            st.info("Você já enviou sua resposta para esta batalha! Aguarde a avaliação do professor.")
            return

        st.markdown("#### Enviar Resposta")
        with st.container(border=True):
            conteudo = st.text_area("Sua solução / código / resposta", height=200, placeholder="Digite ou cole aqui sua resposta...")
            if st.button("Submeter Resposta", use_container_width=True):
                if not conteudo.strip():
                    st.warning("A resposta não pode estar vazia.")
                else:
                    # 🌟 ALTERADO: Envio mapeado no serviço de negócios
                    sucesso, msg = batalha_service.enviar_resposta_batalha(bid, user_id, conteudo)
                    if sucesso:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

    # --------------------------------------------------
    # FLUXO DO PROFESSOR (AVALIAÇÃO DE RESPOSTAS)
    # --------------------------------------------------
    else:
        st.markdown("#### Respostas Recebidas")
        # ALTERADO: Listagem das respostas usando a injeção do repositório
        respostas = batalha_service.listar_respostas_batalha(bid)
        
        if not respostas:
            st.info("Nenhuma resposta enviada por alunos até o momento.")
        else:
            for r in respostas:
                u_info = r.get("usuarios") or {}
                autor  = u_info.get("nome", "Aluno Desconhecido")
                r_id   = r.get("usuario_id")

                with st.expander(f"Resposta de {autor}", expanded=False):
                    st.code(r.get("conteudo", ""))
                    
                    st.markdown("**Avaliação por Critérios:**")
                    criterios = b_atual.get("criterios_avaliacao") or ["Desempenho", "Qualidade do Código", "Estratégia"]
                    
                    notas_criterios = {}
                    col_c1, col_c2 = st.columns(2)
                    
                    for idx, crit in enumerate(criterios):
                        alvo_col = col_c1 if idx % 2 == 0 else col_c2
                        with alvo_col:
                            notas_criterios[crit] = st.slider(f"Nota para: {crit}", 0, 100, 70, key=f"sld_{r.get('id')}_{idx}")

                    if st.button("Lançar Nota da Rodada", key=f"btn_nota_{r.get('id')}", use_container_width=True):
                        # 🌟 ALTERADO: Consolidação e cálculo de notas modularizado
                        ok = batalha_service.lancar_pontuacao_rodada(
                            batalha_id=bid,
                            usuario_id=r_id,
                            rodada=1, # Mapeado para rodada inicial padrão
                            pontos_por_criterio=notas_criterios
                        )
                        if ok:
                            st.success(f"Pontuação de {autor} registrada!")
                            st.rerun()
                        else:
                            st.error("Erro ao salvar pontuação no Supabase.")


def tela_batalha_respostas():
    aplicar_estilo()

    usuario = st.session_state.usuario_logado
    user_id = usuario.get("id")

    cabecalho("Minhas Respostas", "Histórico de submissões em batalhas")

    if st.button("Voltar", key="btn_voltar_resp"):
        st.session_state.pagina = "batalha_de_equipes"
        st.rerun()

    st.divider()

    # ALTERADO: Resgate global de batalhas
    batalhas  = batalha_service.listar_batalhas()
    encontrou = False

    for b in batalhas:
        bid = b.get("id")
        # ALTERADO: Verificação otimizada se o aluno participou daquela rodada
        if not batalha_service.usuario_ja_respondeu(bid, user_id):
            continue
            
        # ALTERADO: Puxa o conteúdo exato salvo da resposta
        respostas = batalha_service.listar_respostas_batalha(bid)
        minha = next((r for r in respostas if r.get("usuario_id") == user_id), None)
        
        if minha:
            encontrou = True
            cor    = "#90caf9" if b.get("finalizada") else #00b4d8"
            status = "Finalizada" if b.get("finalizada") else "Em aberto"
            
            st.markdown(f"""
            <div style="
                background:#f0f9ff;
                border-left:4px solid {cor};
                border-radius:8px;
                padding:14px 18px;
                margin-bottom:10px;
            ">
                <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                    <strong style="color:#0d1b2a;">{b.get('titulo')}</strong>
                    <span style="
                        background:{cor};
                        color:#fff;
                        padding:2px 10px;
                        border-radius:20px;
                        font-size:12px;
                    ">{status}</span>
                </div>
                <p style="color:#333; font-size:13px; margin:0;">{minha.get('conteudo','')}</p>
            </div>
            """, unsafe_allow_html=True)

    if not encontrou:
        st.info("Você ainda não enviou respostas para nenhuma batalha.")