import streamlit as st
import time

def tela_batalha_de_equipes():




# --- Dados mock (substituir por service quando disponivel) ---

TIMES_MOCK = [
    {"id": 1, "nome": "Time Alpha", "membros": ["Ana", "Bruno", "Carlos"]},
    {"id": 2, "nome": "Time Beta",  "membros": ["Diana", "Eduardo", "Fabi"]},
]

BATALHA_MOCK = {
    "id": 1,
    "nome": "Batalha Semana 3",
    "rodadas_totais": 3,
    "rodada_atual": 1,
    "tempo_por_rodada": 60,
    "criterios": "Clareza, Criatividade, Argumentacao",
    "status": "aguardando",
    "placar": {"Time Alpha": 0, "Time Beta": 0},
    "historico": [],
    "penalizacoes": {},
}


# --- Helpers ---

def _init_state():
    defaults = {
        "batalha": dict(BATALHA_MOCK),
        "times": TIMES_MOCK,
        "papel_usuario": None,
        "time_usuario": None,
        "rodada_iniciada": False,
        "tempo_inicio": None,
        "moderador": False,
        "batalha_view": "lobby",
        "alto_contraste": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _segundos_restantes():
    if not st.session_state.tempo_inicio:
        return st.session_state.batalha["tempo_por_rodada"]
    decorrido = time.time() - st.session_state.tempo_inicio
    restante = st.session_state.batalha["tempo_por_rodada"] - decorrido
    return max(0, restante)


def _formatar_tempo(seg):
    m = int(seg) // 60
    s = int(seg) % 60
    return f"{m:02d}:{s:02d}"


def _cor_tempo(seg):
    total = st.session_state.batalha["tempo_por_rodada"]
    pct = seg / total if total else 0
    if pct > 0.5:
        return "green"
    elif pct > 0.2:
        return "orange"
    return "red"


# --- Sub-telas ---

def _tela_lobby():
    st.header("Batalha de Equipes")
    st.caption("Configure a batalha antes de comecar.")

    batalha = st.session_state.batalha

    with st.expander("Definicao do Formato da Batalha", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            rodadas = st.number_input(
                "Numero de rodadas",
                min_value=1, max_value=10,
                value=batalha["rodadas_totais"]
            )
            tempo = st.number_input(
                "Tempo por rodada (segundos)",
                min_value=10, max_value=600,
                value=batalha["tempo_por_rodada"]
            )
        with col2:
            criterios = st.text_area(
                "Criterios de avaliacao",
                value=batalha["criterios"],
                height=100,
                help="Ex: Clareza, Criatividade, Trabalho em equipe"
            )

        if st.button("Salvar formato", use_container_width=True):
            st.session_state.batalha["rodadas_totais"] = rodadas
            st.session_state.batalha["tempo_por_rodada"] = tempo
            st.session_state.batalha["criterios"] = criterios
            st.success("Formato salvo!")

    with st.expander("Regras e Condutas (Fair Play + Anti-trapaca)"):
        st.markdown("""
        **Fair Play**
        - Respeite o tempo de fala de cada equipe.
        - Argumentos devem ser baseados em fatos ou logica.
        - Proibido interromper o time adversario durante sua rodada.

        **Anti-trapaca**
        - Nao e permitido uso de material externo nao autorizado.
        - Qualquer sinal de cola ou auxilio externo resulta em penalizacao.
        - Moderador pode pausar, penalizar ou encerrar a batalha.

        **Moderacao**
        - O moderador tem autoridade maxima durante a batalha.
        - Decisoes do moderador sao finais e irrecorreveis.
        """)

    with st.expander("Sistema de Times", expanded=True):
        st.subheader("Selecione seu Time e Papel")

        nomes_times = [t["nome"] for t in st.session_state.times]
        time_sel = st.selectbox("Seu Time", nomes_times)
        papel_sel = st.selectbox(
            "Seu Papel",
            ["Lider", "Estrategista", "Apoio"],
            help="Lider: porta-voz | Estrategista: define abordagem | Apoio: suporte"
        )

        if st.button("Confirmar ingresso", use_container_width=True):
            st.session_state.time_usuario = time_sel
            st.session_state.papel_usuario = papel_sel
            st.success(f"Voce entrou em **{time_sel}** como **{papel_sel}**!")

        st.divider()
        st.subheader("Times na Batalha")
        for time_item in st.session_state.times:
            with st.container(border=True):
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.markdown(f"**{time_item['nome']}**")
                    st.caption("Membros: " + ", ".join(time_item["membros"]))
                with col_b:
                    placar_val = batalha["placar"].get(time_item["nome"], 0)
                    st.metric("Pontos", placar_val)

    with st.expander("Acesso de Moderador"):
        senha = st.text_input("Senha do moderador", type="password")
        if st.button("Entrar como Moderador"):
            if senha == "mod123":
                st.session_state.moderador = True
                st.success("Acesso de moderador concedido!")
            else:
                st.error("Senha incorreta.")

        if st.session_state.moderador:
            st.info("Voce esta como Moderador.")

    st.divider()

    iniciar = st.button(
        "Iniciar Batalha",
        use_container_width=True,
        type="primary",
        disabled=(not st.session_state.time_usuario)
    )
    if iniciar:
        st.session_state.batalha["status"] = "em_andamento"
        st.session_state.batalha_view = "batalha"
        st.session_state.tempo_inicio = time.time()
        st.session_state.rodada_iniciada = True
        st.rerun()

    if not st.session_state.time_usuario:
        st.caption("Selecione seu time para iniciar.")


def _tela_batalha():
    batalha = st.session_state.batalha
    rodada  = batalha["rodada_atual"]
    total   = batalha["rodadas_totais"]

    st.header(f"Batalha em Andamento — Rodada {rodada}/{total}")
    st.progress(rodada / total, text=f"Rodada {rodada} de {total}")

    restante = _segundos_restantes()
    cor      = _cor_tempo(restante)
    st.markdown(
        f"<h2 style='text-align:center; color:{cor};'>{_formatar_tempo(restante)}</h2>",
        unsafe_allow_html=True
    )
    if restante == 0:
        st.warning("Tempo esgotado! Finalize a rodada.")

    st.divider()

    st.subheader("Placar Atual")
    cols = st.columns(len(st.session_state.times))
    for i, time_item in enumerate(st.session_state.times):
        with cols[i]:
            pontos = batalha["placar"].get(time_item["nome"], 0)
            st.metric(time_item["nome"], pontos)

    st.divider()

    st.subheader("Pontuacao da Rodada")
    st.caption(f"Criterios: {batalha['criterios']}")

    with st.form("form_pontuacao"):
        st.write("Atribuir pontos nesta rodada:")
        pontos_form = {}
        for time_item in st.session_state.times:
            pontos_form[time_item["nome"]] = st.slider(
                f"{time_item['nome']}",
                min_value=0, max_value=10, value=5,
                key=f"pts_{time_item['nome']}"
            )
        submitted = st.form_submit_button("Confirmar pontuacao da rodada")

    if submitted:
        for nome, pts in pontos_form.items():
            batalha["placar"][nome] = batalha["placar"].get(nome, 0) + pts

        batalha["historico"].append({
            "rodada": rodada,
            "pontos": pontos_form.copy()
        })

        if rodada < total:
            batalha["rodada_atual"] += 1
            st.session_state.tempo_inicio = time.time()
            st.success(f"Rodada {rodada} concluida! Iniciando rodada {rodada + 1}...")
        else:
            batalha["status"] = "encerrada"
            st.session_state.batalha_view = "resultados"
            st.success("Batalha encerrada! Veja os resultados.")

        st.rerun()

    st.divider()

    if batalha["historico"]:
        st.subheader("Historico de Rodadas")
        for entrada in batalha["historico"]:
            with st.container(border=True):
                st.markdown(f"**Rodada {entrada['rodada']}**")
                for nome, pts in entrada["pontos"].items():
                    st.write(f"  - {nome}: {pts} pts")
                mvp = max(entrada["pontos"], key=entrada["pontos"].get)
                st.caption(f"MVP da rodada: {mvp}")

    if st.session_state.moderador:
        st.divider()
        st.subheader("Painel do Moderador")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Pausar Rodada", use_container_width=True):
                st.session_state.tempo_inicio = None
                st.session_state.rodada_iniciada = False
                st.warning("Rodada pausada.")

        with col2:
            if st.button("Retomar Rodada", use_container_width=True):
                st.session_state.tempo_inicio = time.time()
                st.session_state.rodada_iniciada = True
                st.success("Rodada retomada.")

        with col3:
            if st.button("Encerrar Batalha", use_container_width=True, type="primary"):
                batalha["status"] = "encerrada"
                st.session_state.batalha_view = "resultados"
                st.rerun()

        st.subheader("Penalizar Time")
        with st.form("form_penalizacao"):
            time_pen  = st.selectbox("Time", [t["nome"] for t in st.session_state.times])
            motivo    = st.text_input("Motivo da penalizacao")
            penalizar = st.form_submit_button("Aplicar Penalizacao")

        if penalizar and motivo:
            if time_pen not in batalha["penalizacoes"]:
                batalha["penalizacoes"][time_pen] = []
            batalha["penalizacoes"][time_pen].append(motivo)
            batalha["placar"][time_pen] = max(0, batalha["placar"].get(time_pen, 0) - 2)
            st.warning(f"{time_pen} penalizado: {motivo} (-2 pts)")
            st.rerun()

    with st.expander("Situacoes Especiais (Conflito, Empate, Desconexao)"):
        situacao = st.selectbox(
            "Tipo de ocorrencia",
            ["Conflito entre times", "Empate", "Desconexao de membro"]
        )
        descricao_sit = st.text_area("Descreva a situacao")
        if st.button("Registrar Ocorrencia"):
            st.info(f"Ocorrencia registrada: **{situacao}** — {descricao_sit}")


def _tela_resultados():
    batalha = st.session_state.batalha

    st.header("Resultados da Batalha")
    st.success("Batalha encerrada!")

    st.subheader("Placar Final")
    placar_ord = sorted(
        batalha["placar"].items(),
        key=lambda x: x[1],
        reverse=True
    )

    for pos, (nome, pts) in enumerate(placar_ord, start=1):
        posicao = f"{pos}o lugar"
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{posicao} — {nome}**")
                pens = batalha["penalizacoes"].get(nome, [])
                if pens:
                    st.caption(f"Penalizacoes: {', '.join(pens)}")
            with col2:
                st.metric("Pontos", pts)

    vencedor = placar_ord[0][0] if placar_ord else "—"
    st.balloons()
    st.markdown(f"### Vencedor: **{vencedor}**")

    st.divider()

    st.subheader("Historico de Rodadas")
    if batalha["historico"]:
        for entrada in batalha["historico"]:
            with st.container(border=True):
                st.markdown(f"**Rodada {entrada['rodada']}**")
                for nome, pts in entrada["pontos"].items():
                    st.write(f"  - {nome}: {pts} pts")
                mvp = max(entrada["pontos"], key=entrada["pontos"].get)
                st.caption(f"MVP: {mvp}")
    else:
        st.info("Nenhuma rodada registrada.")

    st.divider()

    with st.expander("Plano de Testes — Situacoes Especiais"):
        st.markdown("""
        | Cenario | Comportamento esperado |
        |---|---|
        | Conflito entre times | Moderador pausa, registra ocorrencia, retoma |
        | Empate no placar | Sistema exibe empate; moderador desempata manualmente |
        | Desconexao de membro | Rodada pausavel; membro pode reconectar sem perda de dados |
        | Penalizacao | -2 pts aplicados imediatamente; historico registrado |
        | Encerramento antecipado | Moderador encerra; placar parcial e exibido |
        """)

    if st.button("Nova Batalha", use_container_width=True, type="primary"):
        for k in ["batalha", "papel_usuario", "time_usuario",
                  "rodada_iniciada", "tempo_inicio", "moderador", "batalha_view"]:
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()


# --- Entry-point ---

def tela_batalha_de_equipes():

    _init_state()

    if st.session_state.alto_contraste:
        st.markdown(
            """
            <style>
            .stApp { background-color: black; color: white; }
            </style>
            """,
            unsafe_allow_html=True
        )

    view = st.session_state.batalha_view

    if view == "lobby":
        _tela_lobby()

    elif view == "batalha":
        _tela_batalha()

    elif view == "resultados":
        _tela_resultados()
