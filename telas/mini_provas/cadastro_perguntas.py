# telas/mini_provas/cadastro_perguntas.py
import streamlit as st
# 🌟 ALTERADO: Alinhado com a chamada do monólito
from services import mini_prova_service

def tela_cadastro_perguntas():
    st.title("Cadastro de Perguntas")

    disciplina = st.text_input("Disciplina")
    assunto = st.text_input("Assunto")
    
    dificuldade = st.selectbox("Dificuldade", ["facil", "intermediario", "dificil"])
    pergunta = st.text_area("Pergunta")

    st.subheader("Alternativas")
    alternativa_a = st.text_input("Alternativa A")
    alternativa_b = st.text_input("Alternativa B")
    alternativa_c = st.text_input("Alternativa C")
    alternativa_d = st.text_input("Alternativa D")
    alternativa_e = st.text_input("Alternativa E")

    resposta_correta = st.selectbox("Resposta correta", ["A", "B", "C", "D", "E"])

    if st.button("Cadastrar pergunta"):
        usuario = st.session_state.usuario_logado

        dados = {
            "email_professor": usuario["email"],
            "disciplina": disciplina,
            "assunto": assunto,
            "enunciado": pergunta,
            "nivel": dificuldade,
            "alternativa_a": alternativa_a,
            "alternativa_b": alternativa_b,
            "alternativa_c": alternativa_c,
            "alternativa_d": alternativa_d,
            "alternativa_e": alternativa_e,
            "resposta_correta": resposta_correta
        }

        # 🌟 ALTERADO: Execução acionada de forma modular encapsulada
        mini_prova_service.criar_pergunta(dados)
        st.success("Pergunta cadastrada")

    st.divider()
    if st.button("Voltar"):
        st.session_state.pagina = "mini_provas"
        st.rerun()