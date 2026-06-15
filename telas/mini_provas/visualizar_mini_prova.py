# telas/mini_provas/visualizar_mini_prova.py
import streamlit as st
from services import mini_prova_service

def tela_visualizar_mini_prova():
    st.title("Visualizar Mini Prova")
    id_mini_prova = st.session_state.get("id_mini_prova")

    # 🌟 ALTERADO: Chamada via método da classe de serviço
    prova = mini_prova_service.buscar_mini_prova(id_mini_prova)

    if not prova:
        st.error("Mini prova não encontrada")
        return

    st.subheader(prova.get("titulo", "Sem título"))
    st.write(prova.get("descricao", "Sem descrição."))
    
    # 🌟 ALTERADO: Nomenclatura adaptada para as colunas corrigidas no banco PT-BR
    st.write(f"Quantidade de questões: {prova.get('quantidade_questoes', '-')}")
    st.write(f"Duração: {prova.get('duracao_minutos', '-')} minutos")
    st.write(f"Status: {prova.get('status', 'Indisponível')}")

    st.divider()
    if st.button("Voltar"):
        st.session_state.pagina = "mini_provas"
        st.rerun()