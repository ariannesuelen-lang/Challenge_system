import streamlit as st
import time
from conexao import buscar_miniprova
from modules.utils import ir

def render():

    # BUSCA A PROVA DO BANCO
    prova_id = st.session_state.get('prova_id', None)
    if prova_id is None:
        st.error("Nenhuma prova selecionada.")
        if st.button("Voltar"):
            ir('mp_iniciar')
        return

    prova = buscar_miniprova(prova_id).data
    if not prova:
        st.error("Prova não encontrada.")
        return

    prova = prova[0]
    TEMPO_TOTAL = prova["duracao_minutos"] * 60  # converte para segundos

    questoes = [
        # virão do banco futuramente
        {
            "enunciado": "Qual é a capital do Brasil?",
            "alternativas": ["São Paulo", "Brasília", "Rio de Janeiro", "Salvador"],
        },
        {
            "enunciado": "Quanto é 2 + 2?",
            "alternativas": ["3", "4", "5", "6"],
        },
    ]
    total_questoes = len(questoes)

    # INICIALIZA ESTADO
    if 'prova_inicio' not in st.session_state:
        st.session_state.prova_inicio = time.time()
    if 'questao_atual' not in st.session_state:
        st.session_state.questao_atual = 0
    if 'tempo_esgotado' not in st.session_state:
        st.session_state.tempo_esgotado = False
    if 'respostas' not in st.session_state:
        st.session_state.respostas = {}

    # CALCULA TEMPO RESTANTE
    tempo_passado = time.time() - st.session_state.prova_inicio
    tempo_restante = max(0, TEMPO_TOTAL - int(tempo_passado))

    if tempo_restante <= 0:
        st.session_state.tempo_esgotado = True

    # TELA DE TEMPO ESGOTADO
    if st.session_state.tempo_esgotado:
        st.markdown("""
            <div style="
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
                padding: 60px 20px; text-align: center;
            ">
                <div style="
                    background: #111210; border: 0.5px solid #E24B4A;
                    border-radius: 12px; padding: 48px; max-width: 400px;
                ">
                    <div style="font-size: 52px; margin-bottom: 16px;">⏱️</div>
                    <div style="font-size: 20px; font-weight: 500;
                                color: #D3D1C7; margin-bottom: 8px;">
                        Tempo esgotado!
                    </div>
                    <div style="font-size: 14px; color: #888780;">
                        Suas respostas não foram salvas.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Voltar para o início", use_container_width=True):
            st.session_state.pop('prova_inicio', None)
            st.session_state.pop('questao_atual', None)
            st.session_state.pop('tempo_esgotado', None)
            st.session_state.pop('respostas', None)
            st.session_state.pop('prova_id', None)
            ir('mp_iniciar')
        return

    # CRONÔMETRO
    minutos = tempo_restante // 60
    segundos = tempo_restante % 60
    cor_tempo = "#E24B4A" if tempo_restante <= 10 else "#D3D1C7"
    classe_pulso = "cronometro-pulsando" if tempo_restante <= 10 else ""

    st.markdown(f"""
        <div style="
            position: fixed; top: 60px; right: 24px; z-index: 999;
            background: #111210; border: 0.5px solid #2C2C2A;
            border-radius: 8px; padding: 8px 16px;
            display: flex; align-items: center; gap: 8px;
        ">
            <span style="font-size: 13px; color: #5F5E5A;">⏱</span>
            <span class="{classe_pulso}" style="font-size: 15px; font-weight: 500;
                         color: {cor_tempo}; font-variant-numeric: tabular-nums;">
                {minutos:02d}:{segundos:02d}
            </span>
        </div>
    """, unsafe_allow_html=True)

    # PROGRESSO
    questao_idx = st.session_state.questao_atual
    progresso = questao_idx / total_questoes

    st.markdown(f"""
        <div style="margin-bottom: 8px;">
            <span style="font-size: 12px; color: #5F5E5A;">
                Questão {questao_idx + 1} de {total_questoes}
            </span>
        </div>
        <div style="background: #1D1D1B; border-radius: 999px;
                    height: 4px; margin-bottom: 24px;">
            <div style="width: {int(progresso * 100)}%; height: 100%;
                        background: #1D9E75; border-radius: 999px;"></div>
        </div>
    """, unsafe_allow_html=True)

    # QUESTÃO ATUAL
    questao = questoes[questao_idx]
    resposta_salva = st.session_state.respostas.get(questao_idx, None)
    index_salvo = questao["alternativas"].index(resposta_salva) if resposta_salva in questao["alternativas"] else None

    with st.container(border=True):
        st.write(f"**{questao['enunciado']}**")
        escolha = st.radio(
            "Alternativas",
            questao["alternativas"],
            index=index_salvo,
            label_visibility="collapsed",
            key=f"questao_{questao_idx}"
        )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if questao_idx > 0:
            if st.button("← Anterior", use_container_width=True):
                if escolha:
                    st.session_state.respostas[questao_idx] = escolha
                st.session_state.questao_atual -= 1
                st.rerun()

    with col2:
        if questao_idx < total_questoes - 1:
            if st.button("Próxima →", use_container_width=True):
                if escolha is None:
                    st.warning("Selecione uma alternativa antes de continuar.")
                else:
                    st.session_state.respostas[questao_idx] = escolha
                    st.session_state.questao_atual += 1
                    st.rerun()
        else:
            if st.button("Finalizar Prova ✓", use_container_width=True, type="primary"):
                if escolha is None:
                    st.warning("Selecione uma alternativa antes de finalizar.")
                else:
                    st.session_state.respostas[questao_idx] = escolha
                    st.session_state.questao_atual = 0
                    ir('mp_resultado')

    # ATUALIZA A CADA 1 SEGUNDO
    time.sleep(1)
    st.rerun()