import streamlit as st
from services.quiz_ao_vivo_service import (
    criar_quiz,
    adicionar_pergunta,
    alterar_status_quiz,
    entrar_quiz,
    obter_perguntas_quizaovivo,
    responder_pergunta,
    obter_ranking,
    avancar_pergunta,
    repo_get_quiz,
)
from utils.estilo import aplicar_estilo, cabecalho


def tela_quiz_ao_vivo():

    aplicar_estilo()

    usuario = st.session_state.usuario_logado
    tipo    = usuario["tipo_usuario"]

    cabecalho("Quiz ao Vivo", "Participe ou gerencie quizzes em tempo real")

    if tipo == "professor":
        _tela_professor(usuario)
    else:
        _tela_aluno(usuario)


# --------------------------------------------------
# PROFESSOR
# --------------------------------------------------
def _tela_professor(usuario):
    abas = st.tabs(["Criar Quiz", "Adicionar Pergunta", "Controlar Quiz"])

    with abas[0]:
        st.markdown("### Novo Quiz")
        with st.container(border=True):
            titulo = st.text_input("Título do Quiz")
            if st.button("Criar Quiz", use_container_width=True):
                resultado = criar_quiz(titulo, usuario["id"])
                if resultado["sucesso"]:
                    st.success("Quiz criado com sucesso!")
                else:
                    st.error(resultado["mensagem"])

    with abas[1]:
        st.markdown("### Adicionar Pergunta")
        with st.container(border=True):
            quiz_id = st.number_input("ID do Quiz", min_value=1, key="quiz_pergunta")
            texto   = st.text_area("Pergunta")
            col1, col2 = st.columns(2)
            with col1:
                alt1 = st.text_input("Alternativa A")
                alt2 = st.text_input("Alternativa B")
            with col2:
                alt3 = st.text_input("Alternativa C")
                alt4 = st.text_input("Alternativa D")
            alternativas    = [alt1, alt2, alt3, alt4]
            letra_correta   = st.selectbox("Alternativa Correta", ["A", "B", "C", "D"])
            mapa            = {"A": 0, "B": 1, "C": 2, "D": 3}
            indice_correto  = mapa[letra_correta]
            if st.button("Adicionar Pergunta", use_container_width=True):
                resultado = adicionar_pergunta(quiz_id, texto, alternativas, indice_correto)
                if resultado["sucesso"]:
                    st.success("Pergunta adicionada!")
                else:
                    st.error(resultado["mensagem"])

    with abas[2]:
        st.markdown("### Controlar Quiz")
        with st.container(border=True):
            quiz_id_ctrl = st.number_input("ID do Quiz", min_value=1, key="quiz_ctrl")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Abrir", use_container_width=True):
                    alterar_status_quiz(quiz_id_ctrl, "aberto")
                    st.success("Quiz aberto!")
            with col2:
                if st.button("Fechar", use_container_width=True):
                    alterar_status_quiz(quiz_id_ctrl, "fechado")
                    st.success("Quiz fechado!")
            with col3:
                if st.button("Avançar Pergunta", use_container_width=True):
                    avancar_pergunta(quiz_id_ctrl)
                    st.success("Pergunta avançada!")

        st.markdown("### Ranking")
        quiz_id_rank = st.number_input("ID do Quiz para ranking", min_value=1, key="quiz_rank")
        if st.button("Ver Ranking", use_container_width=True):
            ranking = obter_ranking(quiz_id_rank)
            _mostrar_ranking(ranking)


# --------------------------------------------------
# ALUNO
# --------------------------------------------------
def _tela_aluno(usuario):
    with st.container(border=True):
        st.markdown("### Entrar no Quiz")
        quiz_id = st.number_input("ID do Quiz", min_value=1, key="quiz_aluno")
        if st.button("Entrar", use_container_width=True):
            resultado = entrar_quiz(quiz_id, usuario["id"])
            if resultado["sucesso"]:
                st.session_state.quiz_ativo = quiz_id
                st.success("Você entrou no quiz!")
            else:
                st.error(resultado["mensagem"])

    if st.session_state.get("quiz_ativo"):
        quiz_id = st.session_state.quiz_ativo
        st.divider()
        st.markdown("### Perguntas")
        perguntas = obter_perguntas_quizaovivo(quiz_id)
        if perguntas:
            p = perguntas[0]
            st.markdown(f"""
            <div style="
                background:#f0f9ff;
                border-left:4px solid #00b4d8;
                border-radius:8px;
                padding:14px 18px;
                margin-bottom:12px;
            ">
                <strong style="color:#0d1b2a;">{p.get('texto','')}</strong>
            </div>
            """, unsafe_allow_html=True)
            alternativas = p.get("alternativas", [])
            resposta     = st.radio("Escolha uma alternativa", alternativas, key=f"resp_{p.get('id')}")
            indice       = alternativas.index(resposta) if resposta in alternativas else 0
            if st.button("Responder", use_container_width=True):
                resultado = responder_pergunta(quiz_id, p.get("id"), usuario["id"], indice)
                if resultado["sucesso"]:
                    st.success("Resposta enviada!")
                else:
                    st.error(resultado["mensagem"])
        else:
            st.info("Aguardando pergunta do professor...")

        st.divider()
        st.markdown("### Ranking")
        ranking = obter_ranking(quiz_id)
        _mostrar_ranking(ranking)


# --------------------------------------------------
# RANKING
# --------------------------------------------------
def _mostrar_ranking(ranking):
    if not ranking:
        st.info("Sem pontuações ainda.")
        return
    cores = ["#FFD700", "#C0C0C0", "#CD7F32"]
    for i, r in enumerate(ranking):
        cor = cores[i] if i < 3 else "#00b4d8"
        pos = ["1º", "2º", "3º"][i] if i < 3 else f"{i+1}º"
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
            <strong style="color:#0d1b2a;">{pos} — {r.get('nome','')}</strong>
            <span style="color:{cor}; font-weight:700;">{r.get('pontuacao',0)} pts</span>
        </div>
        """, unsafe_allow_html=True)
