import streamlit as st

from services.mini_prova_service import (
    criar_pergunta,
    listar_perguntas_professor
)


def tela_cadastro_perguntas():

    st.title("Cadastro de Perguntas")

    disciplina = st.text_input(
        "Disciplina"
    )

    assunto = st.text_input(
        "Assunto"
    )

    dificuldade = st.selectbox(
        "Dificuldade",
        [
            "facil",
            "intermediario",
            "dificil"
        ]
    )

    pergunta = st.text_area(
        "Pergunta"
    )

    st.subheader("Alternativas")

    alternativa_a = st.text_input(
        "Alternativa A"
    )

    alternativa_b = st.text_input(
        "Alternativa B"
    )

    alternativa_c = st.text_input(
        "Alternativa C"
    )

    alternativa_d = st.text_input(
        "Alternativa D"
    )

    alternativa_e = st.text_input(
        "Alternativa E"
    )

    resposta_correta = st.selectbox(
        "Resposta correta",
        [
            "A",
            "B",
            "C",
            "D",
            "E"
        ]
    )

    if st.button(
        "Cadastrar pergunta"
    ):

        dados = {

            "email_professor": (
                st.session_state
                .usuario_logado["email"]
            ),

            "disciplina": disciplina,

            "assunto": assunto,

            "enunciado": pergunta,

            "nivel": dificuldade,

            "alternativa_a": alternativa_a,
            "alternativa_b": alternativa_b,
            "alternativa_c": alternativa_c,
            "alternativa_d": alternativa_d,
            "alternativa_e": alternativa_e,

            "resposta_correta": (
                resposta_correta
            )
        }

        criar_pergunta(dados)

        st.success(
            "Pergunta cadastrada"
        )

        st.rerun()

    st.divider()

    st.subheader(
        "Perguntas cadastradas"
    )

    perguntas = listar_perguntas_professor(
        st.session_state.usuario_logado[
            "email"
        ]
    )

    if perguntas:

        for pergunta in perguntas:

            with st.container(border=True):

                st.write(
                    pergunta["enunciado"]
                )

                disciplina_nome = (
                    pergunta["disciplinas"]
                    ["nome"]
                )

                tema_nome = (
                    pergunta["temas"]
                    ["nome"]
                )

                st.caption(
                    f"{disciplina_nome} • {tema_nome}"
                )

                st.write(
                    f"Dificuldade: "
                    f"{pergunta['nivel']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "Editar",
                        key=f"editar_"
                        f"{pergunta['id']}"
                    ):

                        st.session_state[
                            "pergunta_edicao"
                        ] = pergunta

                        st.session_state.pagina = (
                            "editar_pergunta"
                        )

                        st.rerun()

                with col2:

                    if st.button(
                        "Excluir",
                        key=f"excluir_"
                        f"{pergunta['id']}"
                    ):

                        st.warning(
                            "Função será criada"
                        )

    else:

        st.info(
            "Nenhuma pergunta cadastrada"
        )

    st.divider()

    if st.button("Voltar"):

        st.session_state.pagina = (
            "mini_provas"
        )

        st.rerun()
