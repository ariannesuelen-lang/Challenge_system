import streamlit as st
from services.batalha_de_equipes_service import (
    listar_batalhas, obter_batalha,
    enviar_resposta_batalha, listar_respostas_batalha,
    usuario_ja_respondeu, finalizar_batalha,
    lancar_pontuacao_rodada, obter_ranking_batalha
)
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

    batalhas = listar_batalhas()
    abertas  = [b for b in batalhas if not b.get("finalizada")]

    if not abertas:
        st.markdown("""
        <div style="
            background:#f0f9ff;
            border-left:4px solid #0d1b2a;
            border-radius:8px;
            padding:14px 18px;
        ">
            <span style="color:#0d1b2a;">Nenhuma batalha em andamento no momento.</span>
        </div>
        """, unsafe_allow_html=True)
        if tipo == "professor":
            if st.button("Criar batalha", use_container_width=True):
                st.session_state.pagina = "batalha_gerenciar"
                st.rerun()
        return

    mapa = {b.get("titulo"): b.get("id") for b in abertas if b.get("titulo")}
    sel  = st.selectbox("Selecione a batalha", list(mapa.keys()))
    bid  = mapa[sel]
    b    = obter_batalha(bid)

    st.markdown(f"""
    <div style="
        background:#f0f9ff;
        border-left:4px solid #00b4d8;
        border-radius:8px;
        padding:14px 18px;
        margin-bottom:12px;
    ">
        <strong style="color:#0d1b2a; font-size:16px;">{b.get('titulo')}</strong>
        {"<br><span style='color:#555; font-size:13px;'>" + b.get('descricao','') + "</span>" if b.get('descricao') else ""}
        {"<br><span style='color:#00b4d8; font-size:12px;'>Prazo: " + str(b.get('prazo','')) + "</span>" if b.get('prazo') else ""}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.metric("Rodadas", b.get("quantidade_rodadas", "-"))
    col2.metric("Tempo por rodada", f"{b.get('tempo_por_rodada_minutos', '-')} min")

    criterios = b.get("criterios_avaliacao") or []

    if b.get("regras_conduta"):
        with st.expander("Regras de conduta"):
            st.write(b["regras_conduta"])

    if criterios:
        with st.expander("Criterios de avaliacao"):
            for c in criterios:
                st.markdown(f"- {c}")

    st.divider()

    # --------------------------------------------------
    # ALUNO
    # --------------------------------------------------
    if tipo == "aluno":

        if usuario_ja_respondeu(bid, user_id):
            st.markdown("""
            <div style="
                background:#e0f7fa;
                border-left:4px solid #00b4d8;
                border-radius:8px;
                padding:12px 16px;
            ">
                <strong style="color:#0d1b2a;">Voce ja enviou sua resposta para esta batalha.</strong>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("### Enviar resposta")
            with st.container(border=True):
                conteudo = st.text_area("Sua resposta", placeholder="Digite sua resposta aqui...")
                if st.button("Enviar resposta", use_container_width=True):
                    if not conteudo or not conteudo.strip():
                        st.warning("Escreva sua resposta antes de enviar.")
                    else:
                        ok, msg = enviar_resposta_batalha(bid, user_id, conteudo)
                        if ok:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)

        st.divider()
        st.markdown("### Ranking atual")
        _mostrar_ranking(bid)

    # --------------------------------------------------
    # PROFESSOR
    # --------------------------------------------------
    else:

        st.markdown("### Respostas recebidas")

        respostas = listar_respostas_batalha(bid)

        if not respostas:
            st.info("Nenhuma resposta enviada ainda.")
        else:
            for r in respostas:
                nome = (r.get("usuarios") or {}).get("nome", f"Usuario {r.get('usuario_id')}")
                st.markdown(f"""
                <div style="
                    background:#f0f9ff;
                    border-left:4px solid #1b3a5c;
                    border-radius:8px;
                    padding:12px 16px;
                    margin-bottom:8px;
                ">
                    <strong style="color:#0d1b2a;">{nome}</strong><br>
                    <span style="color:#333; font-size:13px;">{r.get('conteudo','')}</span><br>
                    <span style="color:#90caf9; font-size:11px;">{r.get('criado_em','')}</span>
                </div>
                """, unsafe_allow_html=True)

        st.divider()
        st.markdown("### Lancar pontuacao por rodada")

        criterios_lista = criterios if criterios else ["Logica", "Organizacao", "Criatividade"]

        with st.container(border=True):
            col1, col2 = st.columns(2)
            with col1:
                aluno_id = st.number_input("ID do aluno", min_value=1, step=1)
            with col2:
                rodada_n = st.number_input(
                    "Rodada",
                    min_value=1,
                    max_value=int(b.get("quantidade_rodadas", 10)),
                    step=1
                )

            pontos_criterio = {}
            for c in criterios_lista:
                pontos_criterio[c] = st.slider(
                    f"Pontuacao: {c}", 0, 100, 70, key=f"crit_{c}_{bid}"
                )

            if st.button("Registrar pontuacao", use_container_width=True):
                if lancar_pontuacao_rodada(bid, aluno_id, rodada_n, pontos_criterio):
                    st.success("Pontuacao registrada!")
                    st.rerun()
                else:
                    st.error("Erro ao registrar pontuacao.")

        st.divider()
        st.markdown("### Ranking atual")
        _mostrar_ranking(bid)

        st.divider()

        if st.button("Finalizar esta batalha", use_container_width=True):
            finalizar_batalha(bid)
            st.success("Batalha finalizada!")
            st.rerun()


def _mostrar_ranking(batalha_id):
    ranking = obter_ranking_batalha(batalha_id)
    if not ranking:
        st.info("Sem pontuacoes registradas ainda.")
        return

    cores = ["#FFD700", "#C0C0C0", "#CD7F32"]

    for i, r in enumerate(ranking):
        cor  = cores[i] if i < 3 else "#00b4d8"
        pos  = ["1o", "2o", "3o"][i] if i < 3 else f"{i+1}o"
        st.markdown(f"""
        <div style="
            background:#f0f9ff;
            border-left:4px solid {cor};
            border-radius:8px;
            padding:10px 16px;
            margin-bottom:6px;
            display:flex;
            justify-content:space-between;
        ">
            <strong style="color:#0d1b2a;">{pos} — {r['nome']}</strong>
            <span style="color:{cor}; font-weight:700;">{r['pontuacao_total']} pts</span>
        </div>
        """, unsafe_allow_html=True)


def tela_batalha_respostas():

    aplicar_estilo()

    usuario = st.session_state.usuario_logado
    user_id = usuario.get("id")

    cabecalho("Minhas Respostas", "Veja as respostas que voce enviou")

    if st.button("Voltar"):
        st.session_state.pagina = "batalha_de_equipes"
        st.rerun()

    st.divider()

    batalhas  = listar_batalhas()
    encontrou = False

    if not batalhas:
        st.info("Nenhuma batalha disponivel.")
        return

    for b in batalhas:
        bid = b.get("id")
        if not usuario_ja_respondeu(bid, user_id):
            continue
        respostas = listar_respostas_batalha(bid)
        minha = next(
            (r for r in respostas if r.get("usuario_id") == user_id), None
        )
        if minha:
            encontrou = True
            cor   = "#90caf9" if b.get("finalizada") else "#00b4d8"
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
                <span style="color:#aaa; font-size:11px;">{minha.get('criado_em','')}</span>
            </div>
            """, unsafe_allow_html=True)

    if not encontrou:
        st.info("Voce ainda nao respondeu nenhuma batalha.")
