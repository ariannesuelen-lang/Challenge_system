import streamlit as st
from services.batalha_de_equipes_service import (
    listar_batalhas, obter_batalha,
    enviar_resposta_batalha, listar_respostas_batalha,
    usuario_ja_respondeu, finalizar_batalha,
    lancar_pontuacao_rodada, obter_ranking_batalha
)


def tela_batalha_rodada():

    usuario = st.session_state.usuario_logado
    tipo    = usuario.get("tipo_usuario", "aluno")
    user_id = usuario.get("id")

    st.title("Batalhas em Andamento")

    if st.button("Voltar"):
        st.session_state.pagina = "batalha_de_equipes"
        st.rerun()

    st.divider()

    batalhas = listar_batalhas()
    abertas  = [b for b in batalhas if not b.get("finalizada")]

    if not abertas:
        st.info("Nenhuma batalha em andamento no momento.")
        if tipo == "professor":
            if st.button("Criar batalha"):
                st.session_state.pagina = "batalha_gerenciar"
                st.rerun()
        return

    mapa = {b.get("titulo"): b.get("id") for b in abertas if b.get("titulo")}
    sel  = st.selectbox("Batalha", list(mapa.keys()))
    bid  = mapa[sel]
    b    = obter_batalha(bid)

    if b.get("prazo"):
        st.caption(f"Prazo: {b['prazo']}")
    if b.get("descricao"):
        st.info(b["descricao"])

    col1, col2 = st.columns(2)
    col1.metric("Rodadas", b.get("quantidade_rodadas", "-"))
    col2.metric("Tempo por rodada", f"{b.get('tempo_por_rodada_minutos', '-')} min")

    if b.get("regras_conduta"):
        with st.expander("Regras de conduta"):
            st.write(b["regras_conduta"])

    criterios = b.get("criterios_avaliacao") or []
    if criterios:
        with st.expander("Criterios de avaliacao"):
            for c in criterios:
                st.markdown(f"- {c}")

    st.divider()

    # --------------------------------------------------
    # ALUNO: envia resposta
    # --------------------------------------------------
    if tipo == "aluno":

        if usuario_ja_respondeu(bid, user_id):
            st.success("Voce ja enviou sua resposta para esta batalha.")
        else:
            st.subheader("Enviar resposta")
            conteudo = st.text_area("Sua resposta")

            if st.button("Enviar"):
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
        st.subheader("Ranking atual")
        _mostrar_ranking(bid)

    # --------------------------------------------------
    # PROFESSOR: ve respostas e lanca pontuacao
    # --------------------------------------------------
    else:

        st.subheader("Respostas recebidas")

        respostas = listar_respostas_batalha(bid)

        if not respostas:
            st.info("Nenhuma resposta enviada ainda.")
        else:
            for r in respostas:
                nome = (r.get("usuarios") or {}).get("nome", f"Usuario {r.get('usuario_id')}")
                with st.container(border=True):
                    st.markdown(f"**{nome}**")
                    st.write(r.get("conteudo", ""))
                    st.caption(str(r.get("criado_em", "")))

        st.divider()
        st.subheader("Lancar pontuacao por rodada")

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

            if st.button("Registrar pontuacao"):
                if lancar_pontuacao_rodada(bid, aluno_id, rodada_n, pontos_criterio):
                    st.success("Pontuacao registrada!")
                    st.rerun()
                else:
                    st.error("Erro ao registrar pontuacao.")

        st.divider()
        st.subheader("Ranking atual")
        _mostrar_ranking(bid)

        st.divider()

        if st.button("Finalizar esta batalha"):
            finalizar_batalha(bid)
            st.success("Batalha finalizada!")
            st.rerun()


def _mostrar_ranking(batalha_id):
    ranking = obter_ranking_batalha(batalha_id)
    if not ranking:
        st.info("Sem pontuacoes registradas ainda.")
        return
    for i, r in enumerate(ranking):
        pos = ["1o", "2o", "3o"][i] if i < 3 else f"{i+1}o"
        st.metric(f"{pos} - {r['nome']}", f"{r['pontuacao_total']} pts")


def tela_batalha_respostas():

    usuario = st.session_state.usuario_logado
    user_id = usuario.get("id")

    st.title("Minhas Respostas")

    if st.button("Voltar"):
        st.session_state.pagina = "batalha_de_equipes"
        st.rerun()

    st.divider()

    batalhas = listar_batalhas()

    if not batalhas:
        st.info("Nenhuma batalha disponivel.")
        return

    encontrou = False

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
            with st.container(border=True):
                status = "Finalizada" if b.get("finalizada") else "Em aberto"
                st.markdown(f"**{b.get('titulo')}** - {status}")
                st.write(minha.get("conteudo", ""))
                st.caption(str(minha.get("criado_em", "")))

    if not encontrou:
        st.info("Voce ainda nao respondeu nenhuma batalha.")
