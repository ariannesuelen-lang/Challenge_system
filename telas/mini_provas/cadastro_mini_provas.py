import streamlit as st
def tela_cadastro_mini_provas():
    st.title("Cadastro de Mini Provas")

    titulo = st.text_input("Título")
    disciplina = st.text_input("Disciplina")
    assunto = st.text_input("Assunto")

    quantidade_total = st.number_input(
        "Quantidade total",
        min_value=1,
        step=1
    )

    quantidade_faceis = st.number_input(
        "Fáceis",
        min_value=0,
        step=1
    )

    quantidade_medias = st.number_input(
        "Médias",
        min_value=0,
        step=1
    )

    quantidade_dificeis = st.number_input(
        "Difíceis",
        min_value=0,
        step=1
    )

    tempo_minutos = st.number_input(
        "Tempo",
        min_value=1,
        step=1
    )

    pontos = st.number_input(
        "Pontuação",
        min_value=0.1,
        step=0.1
    )

    if st.button("Criar Mini Prova"):

        soma = (
            quantidade_faceis +
            quantidade_medias +
            quantidade_dificeis
        )

        if soma != quantidade_total:
            st.error("A soma das dificuldades deve bater")
            return

        dados = {
            "titulo": titulo,
            "disciplina": disciplina,
            "assunto": assunto,
            "quantidade_total": quantidade_total,
            "quantidade_faceis": quantidade_faceis,
            "quantidade_medias": quantidade_medias,
            "quantidade_dificeis": quantidade_dificeis,
            "tempo_minutos": tempo_minutos,
            "pontos": pontos
        }

        criar_mini_prova(dados)

        st.success("Mini prova criada")
