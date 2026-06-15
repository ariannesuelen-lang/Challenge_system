# telas/mini_provas/realizar_mini_prova.py
import streamlit as st
import time
# 🌟 ALTERADO: Consumo mapeado na classe de serviços centralizada
from services import mini_prova_service


def tela_realizar_mini_prova():

    # 🌟 ALTERADO: Busca o ID da prova de forma padronizada no estado da sessão
    prova_id = st.session_state.get('id_mini_prova', None)
    if prova_id is None:
        st.error("Nenhuma prova selecionada.")
        if st.button("Voltar"):
            st.session_state.pagina = "mini_provas"
            st.rerun()
        return

    # 🌟 ALTERADO: Busca os dados através da camada unificada de serviços
    prova = mini_prova_service.buscar_mini_prova(prova_id)
    if not prova:
        st.error("Prova não encontrada.")
        return

    # 🌟 ALTERADO: Nomenclatura ajustada para a coluna em português do banco
    TEMPO_TOTAL = prova.get("duracao_minutos", 30) * 60  

    # Mock de questões (Será substituído dinamicamente pelo banco na evolução do seu TCC)
    questoes = [
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

    # INICIALIZA ESTADO DE EXECUÇÃO
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
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px 20px; text-align: center;">
                <div style="background: #111210; border: 0.5px solid #E24B4A; border-radius: 12px; padding: 48px; max-width: 400px;">
                    <div style="font-size: 52px; margin-bottom: 16px;">⏱️</div>
                    <div style="font-size: 20px; font-weight: 500; color: #D3D1C7; margin-bottom: 8px;">Tempo esgotado!</div>
                    <div style="font-size: 14px; color: #888780;">Suas respostas desta tentativa não puderam ser computadas.</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("Voltar para o início", use_container_width=True):
            st.session_state.pop('prova_inicio', None)
            st.session_state.pop('questao_atual', None)
            st.session_state.pop('tempo_esgotado', None)
            st.session_state.pop('respostas', None)
            st.session_state.pop('id_mini_prova', None)
            st.session_state.pagina = "mini_provas"
            st.rerun()
        return

    # CRONÔMETRO VISUAL
    minutos = tempo_restante // 60
    segundos = tempo_restante % 60
    cor_tempo = "#E24B4A" if tempo_restante <= 15 else "#00b4d8"

    st.markdown(f"""
        <div style="position: fixed; top: 60px; right: 24px; z-index: 999; background: #111210; border: 0.5px solid #2C2C2A; border-radius: 8px; padding: 8px 16px; display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 15px; font-weight: 500; color: {cor_tempo}; font-variant-numeric: tabular-nums;">⏱ {minutos:02d}:{segundos:02d}</span>
        </div>
    """, unsafe_allow_html=True)

    # PROGRESSO DE RESPOSTAS
    questao_idx = st.session_state.questao_atual
    progresso = questao_idx / total_questoes

    st.write(f"**Questão {questao_idx + 1} de {total_questoes}**")
    st.progress(int(progresso * 100))

    # INTERFACE DA QUESTÃO
    questao = questoes[questao_idx]
    resposta_salva = st.session_state.respostas.get(questao_idx, None)
    index_salvo = questao["alternativas"].index(resposta_salva) if resposta_salva in questao["alternativas"] else None

    with st.container(border=True):
        st.write(questao["enunciado"])
        escolha = st.radio(
            "Alternativas",
            questao["alternativas"],
            index=index_salvo,
            label_visibility="collapsed",
            key=f"exec_questao_{questao_idx}"
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
                    st.warning("Selecione uma alternativa antes de concluir.")
                else:
                    st.session_state.respostas[questao_idx] = escolha
                    # Reseta os controles internos e redireciona para a tela de resultados do monólito
                    st.session_state.questao_atual = 0
                    st.session_state.pagina = "resultado_mini_prova"
                    st.rerun()

    time.sleep(1)
    st.rerun()