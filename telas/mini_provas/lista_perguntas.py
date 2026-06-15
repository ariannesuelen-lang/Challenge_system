# telas/mini_provas/lista_perguntas.py
import streamlit as st
# 🌟 ALTERADO: Injeção do serviço global
from services import mini_prova_service

def tela_lista_perguntas():
    st.title("Perguntas cadastradas")

    # 🌟 ALTERADO: Coleta usando a instância única
    perguntas = mini_prova_service.listar_perguntas()

    if not perguntas:
        st.info("Nenhuma pergunta cadastrada")
    else:
        for pergunta in perguntas:
            with st.container(border=True):
                st.write(pergunta.get("enunciado", ""))
                # 🌟 ALTERADO: Mapeamento de 'nivel_dificuldade' (nome correto da coluna unificada no banco)
                st.write(f"Dificuldade: {pergunta.get('nivel_dificuldade', '-')}")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Editar", key=f"editar_{pergunta['id']}"):
                        st.session_state.id_pergunta = pergunta["id"]
                        st.session_state.pagina = "editar_pergunta"
                        st.rerun()
                with col2:
                    if st.button("Excluir", key=f"excluir_{pergunta['id']}"):
                        st.session_state.id_pergunta = pergunta["id"]
                        st.session_state.pagina = "excluir_pergunta"
                        st.rerun()

    st.divider()
    if st.button("Voltar"):
        st.session_state.pagina = "mini_provas"
        st.rerun()