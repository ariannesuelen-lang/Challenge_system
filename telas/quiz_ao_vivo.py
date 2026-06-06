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


def tela_quiz_ao_vivo():
    usuario = st.session_state.usuario_logado
    tipo = usuario["tipo_usuario"]

    st.title("Quiz ao Vivo")

    if tipo == "professor":
        st.subheader("Criar Quiz")

        titulo = st.text_input("Titulo do Quiz")

        if st.button("Criar Quiz"):
            resultado = criar_quiz(titulo, usuario["id"])

            if resultado["sucesso"]:
                st.success("Quiz criado com sucesso!")
            else:
                st.error(resultado["mensagem"])

        st.subheader("Adicionar Pergunta")

        quiz_id = st.number_input(
            "ID do Quiz",
            min_value=1,
            key="quiz_pergunta",
        )

        texto = st.text_area("Pergunta")

        alt1 = st.text_input("Alternativa A")
        alt2 = st.text_input("Alternativa B")
        alt3 = st.text_input("Alternativa C")
        alt4 = st.text_input("Alternativa D")

        alternativas = [alt1, alt2, alt3, alt4]

        letra_correta = st.selectbox(
            "Alternativa Correta",
            ["A", "B", "C", "D"],
        )

        mapa = {
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3,
        }

        indice = mapa[letra_correta]

        if st.button("Adicionar Pergunta"):
            resultado = adicionar_pergunta(
                quiz_id,
                usuario["id"],
                texto,
                alternativas,
                indice,
            )

            if resultado["sucesso"]:
                st.success(f"Pergunta adicionada com sucesso ao Quiz {quiz_id}")
            else:
                st.error(resultado["mensagem"])

        st.subheader("Controlar Quiz")

        quiz_id_controle = st.number_input(
            "Quiz para controlar",
            min_value=1,
            key="quiz_controle",
        )

        col_iniciar, col_proxima, col_finalizar = st.columns(3)

        with col_iniciar:
            if st.button("Iniciar Quiz"):
                resultado = alterar_status_quiz(
                    quiz_id_controle,
                    usuario["id"],
                    "iniciado",
                )

                if resultado["sucesso"]:
                    st.success("Quiz iniciado!")
                    st.rerun()
                else:
                    st.error(resultado["mensagem"])

        with col_proxima:
            if st.button("Proxima Pergunta"):
                resultado = avancar_pergunta(
                    quiz_id_controle,
                    usuario["id"],
                )

                if resultado["sucesso"]:
                    pergunta_atual = resultado["dados"].get("pergunta_atual")
                    st.success(f"Pergunta atual: {pergunta_atual}")
                    st.rerun()
                else:
                    st.error(resultado["mensagem"])

        with col_finalizar:
            if st.button("Finalizar Quiz"):
                resultado = alterar_status_quiz(
                    quiz_id_controle,
                    usuario["id"],
                    "finalizado",
                )

                if resultado["sucesso"]:
                    st.success("Quiz finalizado!")
                    st.rerun()
                else:
                    st.error(resultado["mensagem"])

        quiz = repo_get_quiz(quiz_id_controle)
        if quiz:
            st.info(
                f"Status: {quiz.get('status')} | "
                f"Pergunta atual: {quiz.get('pergunta_atual')}"
            )

    else:
        quiz_id = st.number_input(
            "ID do Quiz",
            min_value=1,
            key="quiz_aluno",
        )

        if st.button("Entrar no Quiz"):
            resultado = entrar_quiz(usuario["id"], quiz_id)

            if resultado["sucesso"]:
                st.session_state[f"participacao_quiz_{quiz_id}"] = (
                    resultado["dados"]["id"]
                )
                st.success("Voce entrou no quiz.")
                st.rerun()
            else:
                st.error(resultado["mensagem"])

        st.button("Atualizar pergunta", key=f"atualizar_quiz_{quiz_id}")

        participacao_id = st.session_state.get(f"participacao_quiz_{quiz_id}")

        if participacao_id:
            quiz = repo_get_quiz(quiz_id)

            if not quiz:
                st.error("Quiz nao encontrado.")
                st.stop()

            if quiz.get("status") == "finalizado":
                st.success("Quiz encerrado!")
                _mostrar_ranking(quiz_id)
                st.stop()

            pergunta_atual = quiz.get("pergunta_atual")

            if quiz.get("status") != "iniciado" or pergunta_atual is None:
                st.info("Aguardando o professor iniciar o quiz.")
                st.stop()

            resultado = obter_perguntas_quizaovivo(quiz_id)

            if not resultado["sucesso"]:
                st.error(resultado.get("mensagem", "Erro ao carregar perguntas"))
                st.stop()

            perguntas = resultado["dados"]
            indice_atual = int(pergunta_atual)

            if indice_atual < 0 or indice_atual >= len(perguntas):
                st.success("Quiz encerrado!")
                _mostrar_ranking(quiz_id)
                st.stop()

            pergunta = perguntas[indice_atual]
            alternativas = pergunta.get("alternativas") or []

            if not alternativas:
                st.error("Pergunta sem alternativas.")
                st.stop()

            st.subheader(f"Pergunta {indice_atual + 1} de {len(perguntas)}")

            escolha = st.radio(
                pergunta["texto"],
                alternativas,
                key=f"quiz_{quiz_id}_pergunta_{pergunta['id']}",
            )

            if st.button("Responder", key=f"resp_{quiz_id}_{pergunta['id']}"):
                indice_resposta = alternativas.index(escolha)

                retorno = responder_pergunta(
                    participacao_id,
                    pergunta["id"],
                    indice_resposta,
                )

                if retorno["sucesso"]:
                    st.success(retorno["dados"]["feedback"])
                    st.info(
                        f"Sua pontuacao: "
                        f"{retorno['dados']['pontuacao']} pontos"
                    )
                else:
                    st.error(retorno["mensagem"])

        st.divider()

    quiz_ranking = st.number_input(
        "Quiz Ranking",
        min_value=1,
        key="ranking",
    )

    if st.button("Ver Ranking"):
        _mostrar_ranking(quiz_ranking)


def _mostrar_ranking(quiz_id):
    resultado = obter_ranking(quiz_id)

    if resultado["sucesso"]:
        st.subheader("Ranking")

        for posicao, jogador in enumerate(resultado["dados"], start=1):
            usuario = jogador.get("usuarios") or {}
            nome = usuario.get("nome", "Aluno")

            st.write(
                f"{posicao} lugar - "
                f"{nome} - "
                f"{jogador['pontuacao']} pontos"
            )
    else:
        st.error(resultado["mensagem"])
