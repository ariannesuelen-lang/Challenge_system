import streamlit as st
from services.batalha_de_equipes_service import (
    criar_time, listar_times, entrar_no_time,
    listar_membros_time, time_do_usuario,
    criar_batalha, listar_batalhas, buscar_batalha,
    atualizar_status_batalha, registrar_pontuacao,
    calcular_placar, calcular_mvp, listar_pontuacoes_batalha
)


# ==========================================
# SEÇÃO: TIMES
# ==========================================

def _secao_times():
    usuario = st.session_state.usuario_logado
    usuario_id = usuario["id"]

    st.subheader("⚔️ Sistema de Times")

    meu_time = time_do_usuario(usuario_id)

    if meu_time:
        time_info = meu_time.get("times", {})
        time_id = time_info.get("id")
        time_nome = time_info.get("nome", "Meu Time")

        with st.container(border=True):
            st.markdown(f"### 🛡️ Seu Time: **{time_nome}**")
            st.caption(f"Seu papel: **{meu_time.get('papel', 'membro').capitalize()}**")

            membros = listar_membros_time(time_id)
            if membros:
                st.write(f"**Membros ({len(membros)}):**")
                for m in membros:
                    nome_membro = m.get("usuarios", {}).get("nome", "—")
                    papel = m.get("papel", "membro")
                    icone = "👑" if papel == "lider" else "👤"
                    st.write(f"{icone} {nome_membro} — *{papel.capitalize()}*")
            else:
                st.info("Nenhum membro encontrado.")
    else:
        st.info("Você ainda não faz parte de nenhum time.")

        tab_criar, tab_entrar = st.tabs(["➕ Criar Time", "🚪 Entrar em Time"])

        with tab_criar:
            st.write("Crie seu próprio time e convide colegas.")
            nome_novo = st.text_input("Nome do time", max_chars=50, key="input_criar_time")
            if st.button("Criar Time", key="btn_criar_time"):
                if not nome_novo.strip():
                    st.error("Informe um nome para o time.")
                else:
                    resultado = criar_time(nome_novo, usuario_id)
                    if resultado["sucesso"]:
                        st.success(f"Time **{nome_novo}** criado com sucesso! Você é o líder.")
                        st.rerun()
                    else:
                        st.error(resultado["mensagem"])

        with tab_entrar:
            times = listar_times()
            if not times:
                st.info("Nenhum time disponível no momento.")
            else:
                opcoes = {t["nome"]: t["id"] for t in times}
                escolha = st.selectbox("Selecione um time", list(opcoes.keys()), key="sel_entrar_time")
                if st.button("Entrar no Time", key="btn_entrar_time"):
                    resultado = entrar_no_time(opcoes[escolha], usuario_id)
                    if resultado["sucesso"]:
                        st.success(f"Você entrou no time **{escolha}**!")
                        st.rerun()
                    else:
                        st.error(resultado["mensagem"])

    st.divider()
    if st.button("← Voltar ao Hub", key="btn_voltar_times"):
        st.session_state.batalha_sub_pagina = "hub"
        st.rerun()


# ==========================================
# SEÇÃO: CRIAR BATALHA
# ==========================================

def _secao_criar_batalha():
    st.title("🗡️ Criar Nova Batalha")
    st.caption("Configure os parâmetros da batalha entre dois times.")

    times = listar_times()
    if len(times) < 2:
        st.warning("É necessário ter pelo menos 2 times cadastrados para criar uma batalha.")
        if st.button("← Voltar", key="btn_voltar_criar"):
            st.session_state.batalha_sub_pagina = "hub"
            st.rerun()
        return

    opcoes_times = {t["nome"]: t["id"] for t in times}
    nomes_times = list(opcoes_times.keys())

    with st.form("form_criar_batalha"):
        st.subheader("📝 Definição do Formato")
        titulo = st.text_input("Título da batalha *", max_chars=80)
        descricao = st.text_area("Descrição / critérios gerais", max_chars=300)

        col1, col2 = st.columns(2)
        with col1:
            rodadas = st.number_input("Número de rodadas", min_value=1, max_value=10, value=3)
        with col2:
            tempo_rodada = st.number_input("Tempo por rodada (min)", min_value=1, max_value=60, value=10)

        st.divider()
        st.subheader("🛡️ Times Participantes")
        col3, col4 = st.columns(2)
        with col3:
            time_a_nome = st.selectbox("Time A 🔵", nomes_times, key="sel_time_a")
        with col4:
            opcoes_b = [n for n in nomes_times if n != time_a_nome]
            time_b_nome = st.selectbox("Time B 🔴", opcoes_b, key="sel_time_b")

        st.divider()
        st.subheader("📜 Regras e Conduta")
        st.info(
            "**Fair play obrigatório:** Respostas devem ser originais. "
            "Plágio ou trapaça resulta em penalização automática. "
            "O moderador pode pausar, penalizar ou encerrar a batalha a qualquer momento."
        )

        enviado = st.form_submit_button("✅ Criar Batalha")

    if enviado:
        if not titulo.strip():
            st.error("Informe o título da batalha.")
        elif time_a_nome == time_b_nome:
            st.error("Os times devem ser diferentes.")
        else:
            usuario = st.session_state.usuario_logado
            resultado = criar_batalha(
                titulo=titulo,
                descricao=descricao,
                criador_id=usuario["id"],
                time_a_id=opcoes_times[time_a_nome],
                time_b_id=opcoes_times[time_b_nome],
                rodadas=rodadas,
                tempo_rodada=tempo_rodada
            )
            if resultado["sucesso"]:
                st.success(f"Batalha **{titulo}** criada com sucesso!")
                st.session_state.batalha_sub_pagina = "hub"
                st.rerun()
            else:
                st.error(resultado["mensagem"])

    if st.button("← Voltar", key="btn_voltar_criar_bottom"):
        st.session_state.batalha_sub_pagina = "hub"
        st.rerun()


# ==========================================
# SEÇÃO: BATALHA EM RODADA
# ==========================================

def _secao_batalha_rodada():
    usuario = st.session_state.usuario_logado
    batalha_id = st.session_state.get("batalha_selecionada_id")

    if not batalha_id:
        st.warning("Nenhuma batalha selecionada.")
        if st.button("← Voltar", key="btn_voltar_rodada_vazia"):
            st.session_state.batalha_sub_pagina = "hub"
            st.rerun()
        return

    batalha = buscar_batalha(batalha_id)
    if not batalha:
        st.error("Batalha não encontrada.")
        return

    time_a = batalha.get("times_a", {})
    time_b = batalha.get("times_b", {})
    time_a_id = time_a.get("id")
    time_b_id = time_b.get("id")
    time_a_nome = time_a.get("nome", "Time A")
    time_b_nome = time_b.get("nome", "Time B")

    rodada_atual = batalha.get("rodada_atual", 0)
    rodadas_total = batalha.get("rodadas_total", 3)
    status = batalha.get("status", "aguardando")

    st.title(f"⚔️ {batalha['titulo']}")
    st.caption(batalha.get("descricao", ""))

    pontos_a, pontos_b = calcular_placar(batalha_id, time_a_id, time_b_id)
    col1, col_vs, col2 = st.columns([2, 1, 2])
    with col1:
        st.metric(f"🔵 {time_a_nome}", pontos_a)
    with col_vs:
        st.markdown("<h3 style='text-align:center;margin-top:18px'>VS</h3>", unsafe_allow_html=True)
    with col2:
        st.metric(f"🔴 {time_b_nome}", pontos_b)

    st.divider()

    status_label = {
        "aguardando": "⏳ Aguardando início",
        "em_andamento": "🟢 Em andamento",
        "pausada": "⏸️ Pausada",
        "encerrada": "🏁 Encerrada"
    }
    st.info(f"Status: {status_label.get(status, status)} | Rodada: {rodada_atual}/{rodadas_total}")

    if usuario.get("tipo_usuario") in ("professor", "admin"):
        st.subheader("🎮 Painel do Moderador")
        col_a, col_b, col_c, col_d = st.columns(4)

        with col_a:
            if status == "aguardando" and st.button("▶️ Iniciar Batalha"):
                atualizar_status_batalha(batalha_id, "em_andamento", 1)
                st.success("Batalha iniciada!")
                st.rerun()

        with col_b:
            if status == "em_andamento" and st.button("⏸️ Pausar"):
                atualizar_status_batalha(batalha_id, "pausada")
                st.warning("Batalha pausada.")
                st.rerun()

        with col_c:
            if status == "pausada" and st.button("▶️ Retomar"):
                atualizar_status_batalha(batalha_id, "em_andamento")
                st.success("Batalha retomada!")
                st.rerun()

        with col_d:
            if status in ("em_andamento", "pausada") and st.button("🏁 Encerrar"):
                atualizar_status_batalha(batalha_id, "encerrada")
                st.success("Batalha encerrada!")
                st.rerun()

        if status == "em_andamento":
            st.divider()
            st.subheader("➕ Registrar Pontuação")
            col_p1, col_p2 = st.columns(2)

            with col_p1:
                time_pontuar = st.selectbox(
                    "Time", [time_a_nome, time_b_nome], key="sel_time_pontuar"
                )
                pontos_add = st.number_input("Pontos", min_value=1, max_value=100, value=10, key="inp_pontos")
                rodada_reg = st.number_input(
                    "Rodada", min_value=1, max_value=rodadas_total, value=rodada_atual, key="inp_rodada"
                )

            with col_p2:
                motivo = st.text_area("Motivo / critério", max_chars=200, key="txt_motivo")
                if st.button("✅ Confirmar Pontuação"):
                    tid = time_a_id if time_pontuar == time_a_nome else time_b_id
                    resultado = registrar_pontuacao(batalha_id, tid, rodada_reg, pontos_add, motivo)
                    if resultado["sucesso"]:
                        st.success(f"+{pontos_add} ponto(s) para **{time_pontuar}**!")
                        st.rerun()
                    else:
                        st.error(resultado["mensagem"])

            if st.button("➡️ Próxima Rodada"):
                nova_rodada = rodada_atual + 1
                if nova_rodada > rodadas_total:
                    atualizar_status_batalha(batalha_id, "encerrada", nova_rodada)
                    st.success("Última rodada concluída. Batalha encerrada!")
                else:
                    atualizar_status_batalha(batalha_id, "em_andamento", nova_rodada)
                    st.success(f"Iniciando rodada {nova_rodada}!")
                st.rerun()

    st.divider()
    st.subheader("📋 Histórico de Pontuações")
    pontuacoes = listar_pontuacoes_batalha(batalha_id)
    if pontuacoes:
        for rod in range(1, rodadas_total + 1):
            pts_rod = [p for p in pontuacoes if p.get("rodada") == rod]
            if pts_rod:
                with st.expander(f"Rodada {rod}"):
                    for p in pts_rod:
                        time_nome_p = p.get("times", {}).get("nome", f"Time {p['time_id']}")
                        motivo_txt = f" — {p['motivo']}" if p.get("motivo") else ""
                        st.write(f"🏅 **{time_nome_p}**: +{p['pontos']} pt(s){motivo_txt}")
    else:
        st.info("Nenhuma pontuação registrada ainda.")

    st.divider()
    if st.button("← Voltar às Batalhas", key="btn_voltar_rodada"):
        st.session_state.batalha_sub_pagina = "hub"
        st.rerun()


# ==========================================
# SEÇÃO: RESULTADOS
# ==========================================

def _secao_resultados():
    st.title("🏆 Resultados das Batalhas")

    batalhas = listar_batalhas()
    encerradas = [b for b in batalhas if b.get("status") == "encerrada"]

    if not encerradas:
        st.info("Nenhuma batalha encerrada ainda.")
        if st.button("← Voltar", key="btn_voltar_resultados_vazio"):
            st.session_state.batalha_sub_pagina = "hub"
            st.rerun()
        return

    for batalha in encerradas:
        time_a = batalha.get("times_a", {})
        time_b = batalha.get("times_b", {})
        time_a_id = time_a.get("id")
        time_b_id = time_b.get("id")
        time_a_nome = time_a.get("nome", "Time A")
        time_b_nome = time_b.get("nome", "Time B")

        pontos_a, pontos_b = calcular_placar(batalha["id"], time_a_id, time_b_id)
        vencedor = time_a_nome if pontos_a > pontos_b else (
            time_b_nome if pontos_b > pontos_a else "Empate"
        )

        with st.container(border=True):
            st.markdown(f"### {batalha['titulo']}")
            col1, col_vs, col2 = st.columns([2, 1, 2])
            with col1:
                st.metric(f"🔵 {time_a_nome}", pontos_a,
                          delta="🏆 Vencedor" if vencedor == time_a_nome else None)
            with col_vs:
                st.markdown("<p style='text-align:center;margin-top:18px;font-weight:bold'>VS</p>",
                            unsafe_allow_html=True)
            with col2:
                st.metric(f"🔴 {time_b_nome}", pontos_b,
                          delta="🏆 Vencedor" if vencedor == time_b_nome else None)

            if vencedor == "Empate":
                st.warning("🤝 Resultado: **Empate!**")
            else:
                st.success(f"🏆 Vencedor: **{vencedor}**")

            mvp = calcular_mvp(batalha["id"])
            if mvp:
                mvp_nome = mvp.get("usuarios", {}).get("nome", "—")
                st.info(f"⭐ MVP: **{mvp_nome}** — {mvp.get('pontos', 0)} pts de contribuição")

            with st.expander("Ver detalhes por rodada"):
                pontuacoes = listar_pontuacoes_batalha(batalha["id"])
                rodadas_total = batalha.get("rodadas_total", 3)
                for rod in range(1, rodadas_total + 1):
                    pts = [p for p in pontuacoes if p.get("rodada") == rod]
                    if pts:
                        st.write(f"**Rodada {rod}:**")
                        for p in pts:
                            tnome = p.get("times", {}).get("nome", f"Time {p['time_id']}")
                            st.write(f"  • {tnome}: +{p['pontos']} pt(s)"
                                     + (f" — {p['motivo']}" if p.get("motivo") else ""))

    st.divider()
    if st.button("← Voltar", key="btn_voltar_resultados"):
        st.session_state.batalha_sub_pagina = "hub"
        st.rerun()


# ==========================================
# TELA PRINCIPAL (roteador)
# ==========================================

def tela_batalha_de_equipes():

    sub = st.session_state.get("batalha_sub_pagina", "hub")

    if sub == "batalha_rodada":
        _secao_batalha_rodada()
        return

    if sub == "criar_batalha":
        _secao_criar_batalha()
        return

    if sub == "resultados":
        _secao_resultados()
        return

    if sub == "times":
        _secao_times()
        return

    # ── HUB ────────────────────────────────────────────────────────
    usuario = st.session_state.usuario_logado
    eh_professor = usuario.get("tipo_usuario") in ("professor", "admin")

    st.title("⚔️ Batalha de Equipes")
    st.caption("Colaboração, estratégia e fair play em rodadas de desafio entre times.")

    nav_cols = st.columns(4)
    with nav_cols[0]:
        if st.button("🛡️ Meu Time", use_container_width=True):
            st.session_state.batalha_sub_pagina = "times"
            st.rerun()
    with nav_cols[1]:
        if st.button("🏆 Resultados", use_container_width=True):
            st.session_state.batalha_sub_pagina = "resultados"
            st.rerun()
    if eh_professor:
        with nav_cols[2]:
            if st.button("➕ Nova Batalha", use_container_width=True):
                st.session_state.batalha_sub_pagina = "criar_batalha"
                st.rerun()

    st.divider()

    st.subheader("📋 Batalhas")
    batalhas = listar_batalhas()

    tab_all, tab_ag, tab_em, tab_pau, tab_enc = st.tabs(
        ["Todas", "⏳ Aguardando", "🟢 Em andamento", "⏸️ Pausadas", "🏁 Encerradas"]
    )

    def _renderizar_lista(lista):
        if not lista:
            st.info("Nenhuma batalha nesta categoria.")
            return
        for b in lista:
            time_a_nome = b.get("times_a", {}).get("nome", "Time A")
            time_b_nome = b.get("times_b", {}).get("nome", "Time B")
            status = b.get("status", "aguardando")
            rodada_atual = b.get("rodada_atual", 0)
            rodadas_total = b.get("rodadas_total", 3)
            status_label = {
                "aguardando": "⏳ Aguardando",
                "em_andamento": "🟢 Em andamento",
                "pausada": "⏸️ Pausada",
                "encerrada": "🏁 Encerrada"
            }
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{b['titulo']}**")
                    st.caption(
                        f"🔵 {time_a_nome}  vs  🔴 {time_b_nome}  |  "
                        f"Rodada {rodada_atual}/{rodadas_total}  |  "
                        f"{status_label.get(status, status)}"
                    )
                    if b.get("descricao"):
                        st.write(b["descricao"])
                with col2:
                    label_btn = "🎮 Entrar" if status == "em_andamento" else "👁️ Ver"
                    if st.button(label_btn, key=f"btn_batalha_{b['id']}"):
                        st.session_state.batalha_selecionada_id = b["id"]
                        st.session_state.batalha_sub_pagina = "batalha_rodada"
                        st.rerun()

    mapa_status = {
        "⏳ Aguardando": "aguardando",
        "🟢 Em andamento": "em_andamento",
        "⏸️ Pausadas": "pausada",
        "🏁 Encerradas": "encerrada"
    }

    with tab_all:
        _renderizar_lista(batalhas)

    for tab_obj, st_val in zip(
        [tab_ag, tab_em, tab_pau, tab_enc],
        mapa_status.values()
    ):
        with tab_obj:
            _renderizar_lista([b for b in batalhas if b.get("status") == st_val])
