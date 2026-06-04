import streamlit as st

from services.quiz_ao_vivo_service import (
    criar_quiz,
    adicionar_pergunta,
    alterar_status_quiz,
    entrar_quiz,
    obter_perguntas_quizaovivo,
    responder_pergunta,
    obter_ranking
)

def tela_quiz_ao_vivo():

    usuario = st.session_state.usuario_logado

    tipo = usuario["tipo_usuario"]
    st.title("Quiz ao Vivo")

    if tipo == "professor":
        st.subheader("Criar Quiz")

        titulo = st.text_input("Título do Quiz")
        if st.button("Criar Quiz"):

            resultado = criar_quiz(
                titulo,
                usuario["id"]
            )

            if resultado["sucesso"]:
                st.success("Quiz criado com sucesso!")

            else:
                st.error(resultado["mensagem"])

        st.subheader("Adicionar Pergunta")

        quiz_id = st.number_input(
            "ID do Quiz",
            min_value=1
        )

        texto = st.text_area(
            "Pergunta"
        )

        alt1 = st.text_input("Alternativa A")
        alt2 = st.text_input("Alternativa B")
        alt3 = st.text_input("Alternativa C")
        alt4 = st.text_input("Alternativa D")

        alternativas = [
            alt1,
            alt2,
            alt3,
            alt4
        ]

        letra_correta = st.selectbox(
            "Alternativa Correta",
            ["A", "B", "C", "D"]
        )

        mapa = {
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3
        }

        indice = mapa[letra_correta]

        if st.button("Adicionar Pergunta"):

            resultado = adicionar_pergunta(
                quiz_id,
                usuario["id"],
                texto,
                alternativas,
                indice
            )
            if resultado["sucesso"]:
                st.success(
                    f"Quiz criado com ID {resultado['dados']['id']}"
                )
            else:
                st.error(resultado["mensagem"])

        quiz_id_inicio = st.number_input(
            "Quiz para iniciar",
            min_value=1,
            key="inicio"
        )

        if st.button("Iniciar Quiz"):

            resultado = alterar_status_quiz(
                quiz_id_inicio,
                usuario["id"],
                "iniciado"
            )

            if resultado["sucesso"]:
                st.success("Quiz iniciado!")

            else:
                st.error(resultado["mensagem"])

        quiz_id_final = st.number_input(
            "Quiz para finalizar",
            min_value=1,
            key="fim"
        )

        if st.button("Finalizar Quiz"):

            resultado = alterar_status_quiz(
                quiz_id_final,
                usuario["id"],
                "finalizado"
            )

            if resultado["sucesso"]:
                st.success("Quiz finalizado!")

            else:
                st.error(resultado["mensagem"])

    else:
        quiz_id = st.number_input(
            "ID do Quiz",
            min_value=1
        )

        if st.button("Entrar no Quiz"):

            resultado = entrar_quiz(
                usuario["id"],
                quiz_id
            )

            st.write(resultado)

            if resultado["sucesso"]:

                st.session_state.participacao = (
                    resultado["dados"]["id"]
                )

                st.success("Entrou no Quiz!")


            else:

                st.error(resultado["mensagem"])

        if "participacao" in st.session_state:

            resultado = obter_perguntas_quizaovivo(
                quiz_id
            )

            if resultado["sucesso"]:

                for pergunta in resultado["dados"]:

                    st.write(pergunta["texto"])

                    escolha = st.radio(
                        pergunta["texto"],
                        pergunta["alternativas"],
                        key=pergunta["id"]
                    )

                    if st.button(
                            "Responder",
                            key=f"resp_{pergunta['id']}"
                    ):

                        indice = pergunta["alternativas"].index(
                            escolha
                        )

                        retorno = responder_pergunta(
                            st.session_state.participacao,
                            pergunta["id"],
                            indice
                        )

                        if retorno["sucesso"]:
                            st.success(
                                retorno["dados"]["feedback"]
                            )
                        else:
                            st.error(
                                retorno["mensagem"]
                            )

            else:

                st.error(
                    resultado.get(
                        "mensagem",
                        "Erro ao carregar perguntas"
                    )
                )

        st.divider()

    quiz_ranking = st.number_input(
        "Quiz Ranking",
        min_value=1,
        key="ranking"
    )

    if st.button("Ver Ranking"):

        resultado = obter_ranking(
            quiz_ranking
        )

        if resultado["sucesso"]:

            st.subheader("🏆 Ranking")

            for posicao, jogador in enumerate(
                    resultado["dados"],
                    start=1
            ):
                st.write(
                    f"{posicao}º lugar - "
                    f"{jogador['pontuacao']} pontos"
                )

        else:

            st.error(
                resultado["mensagem"]
            )
