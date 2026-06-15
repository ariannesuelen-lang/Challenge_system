# telas/mini_provas/historico_provas.py
import streamlit as st

def tela_historico_provas():
    st.title("Meu Histórico de Provas")
    st.subheader("Mini-provas finalizadas por você")

    # Simulando a listagem de tentativas (futuramente virá do banco)
    for i in range(3):
        with st.container(border=True):
            st.markdown(f"#### 📝 Mini Prova de Engenharia {i+1}")
            st.write("Nota final: **8.0** | Pontuação extra: **0.8**")

            # Ao clicar, envia o ID específico para a sessão e muda para a tela de detalhes
            if st.button(f"Ver Gabarito Detalhado", key=f"btn_gabarito_{i}", use_container_width=True):
                st.session_state.id_prova_concluida = i
                st.session_state.pagina = "detalhe_gabarito" # 🌟 Rota atualizada e clara
                st.rerun()

    st.divider()
    if st.button("Voltar"):
        st.session_state.pagina = "mini_provas"
        st.rerun()