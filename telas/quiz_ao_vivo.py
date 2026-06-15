# telas/quiz_ao_vivo.py
import streamlit as st
from services import quiz_service
from utils.estilo import aplicar_estilo, cabecalho

def tela_quiz_ao_vivo():
    aplicar_estilo()

    usuario = st.session_state.get("usuario_logado", {})
    tipo = usuario.get("tipo_usuario", "aluno")
    user_id = usuario.get("id")

    cabecalho(
        "Quiz ao Vivo",
        "Responda às perguntas em tempo real ou gerencie as rodadas ativas"
    )

    if tipo == "professor":
        st.subheader("Criar Quiz")
        titulo = st.text_input("Título do Quiz")

        if st.button("Criar Quiz", use_container_width=True):
            # 🌟 ALTERADO: Chamadas convertidas para o serviço encapsulado
            resultado = quiz_service.criar_quiz(titulo, user_id)
            if resultado["sucesso"]:
                st.success("Quiz criado com sucesso!")
            else:
                st.error(resultado["mensagem"])

        st.subheader("Adicionar Pergunta")
        quiz_id = st.number_input("ID do Quiz", min_value=1, key="quiz_pergunta")
        texto = st.text_area("Pergunta")

        alt1 = st.text_input("Alternativa A")
        alt2 = st.text_input("Alternativa B")
        alt3 = st.text_input("Alternativa C")
        alt4 = st.text_input("Alternativa D")
        alternativas = [alt1, alt2, alt3, alt4]

        letra_correta = st.selectbox("Alternativa Correta", ["A", "B", "C", "D"])
        mapa = {"A": 0, "B": 1, "C": 2, "D": 3}
        indice = mapa[letra_correta]

        if st.button("Adicionar Pergunta", use_container_width=True):
            resultado = quiz_service.adicionar_pergunta(quiz_id, user_id, texto, alternativas, indice)
            if resultado["sucesso"]:
                st.success(f"Pergunta adicionada com sucesso ao Quiz {quiz_id}")
            else:
                st.error(resultado["mensagem"])

        st.subheader("Controlar Quiz")
        quiz_id_controle = st.number_input("Quiz para controlar", min_value=1, key="quiz_controle")

        col_iniciar, col_proxima, col_finalizar = st.columns(3)

        with col_iniciar:
            if st.button("Iniciar Quiz", use_container_width=True):
                resultado = quiz_service.alterar_status_quiz(quiz_id_controle, user_id, "iniciado")
                if resultado["sucesso"]:
                    st.success("Quiz iniciado!")
                    st.rerun()
                else:
                    st.error(resultado["mensagem"])

        with col_proxima:
            if st.button("Próxima Pergunta", use_container_width=True):
                resultado = quiz_service.avancar_pergunta(quiz_id_controle, user_id)
                if resultado["sucesso"]:
                    st.success("Avançado com sucesso para a próxima rodada!")
                    st.rerun()
                else:
                    st.error(resultado["mensagem"])

        with col_finalizar:
            if st.button("Finalizar Quiz", use_container_width=True):
                resultado = quiz_service.alterar_status_quiz(quiz_id_controle, user_id, "finalizado")
                if resultado["sucesso"]:
                    st.success("Quiz finalizado!")
                    st.rerun()
                else:
                    st.error(resultado["mensagem"])

        # 🌟 ALTERADO: Consulta o status de forma segura usando o repositório embutido na classe
        dados_quiz_res = quiz_service.quiz_repo.obter_quiz(quiz_id_controle)
        if dados_quiz_res and dados_quiz_res.data:
            quiz = dados_quiz_res.data[0]
            st.markdown(f"""
            <div style="background: #f0f9ff; border-left: 4px solid #00b4d8; border-radius: 8px; padding: 12px 16px; margin-top: 15px;">
                <span style="color: #0d1b2a; font-weight: 600;">Status Atual: {quiz.get('status', '-')}</span><br>
                <span style="color: #555; font-size: 13px;">Pergunta Atual (Índice): {quiz.get('pergunta_atual', '-')}</span>
            </div>
            """, unsafe_allow_html=True)

    else:
        quiz_id = st.number_input("ID do Quiz", min_value=1, key="quiz_aluno")

        if st.button("Entrar no Quiz", use_container_width=True):
            resultado = quiz_service.entrar_quiz(user_id, quiz_id)
            if resultado["sucesso"]:
                st.session_state[f"participacao_quiz_{quiz_id}"] = resultado["dados"]["id"]
                st.success("Você entrou no quiz!")
                st.rerun()
            else:
                st.error(resultado["mensagem"])

        st.button("Atualizar pergunta", key=f"atualizar_quiz_{quiz_id}", use_container_width=True)
        participacao_id = st.session_state.get(f"participacao_quiz_{quiz_id}")

        if participacao_id:
            dados_quiz_res = quiz_service.quiz_repo.obter_quiz(quiz_id)
            if not dados_quiz_res or not dados_quiz_res.data:
                st.error("Quiz não encontrado.")
                st.stop()
                
            quiz = dados_quiz_res.data[0]

            if quiz.get("status") == "finalizado":
                st.success("Quiz encerrado!")
                _mostrar_ranking(quiz_id)
                st.stop()

            # 🌟 ALTERADO: Consome o motor dinâmico e o gabarito protegido pela classe de serviço
            info_pergunta = quiz_service.obter_pergunta_atual_quiz(quiz_id)
            if not info_pergunta["sucesso"] or info_pergunta["dados"]["fim"]:
                st.success("Quiz encerrado ou aguardando rodadas!")
                _mostrar_ranking(quiz_id)
                st.stop()

            pergunta = info_pergunta["dados"]["pergunta"]
            if not pergunta:
                st.info("Aguardando o professor iniciar o quiz.")
                st.stop()

            alternativas = pergunta.get("alternativas") or []
            st.subheader(f"Pergunta {info_pergunta['dados']['indice'] + 1} de {info_pergunta['dados']['total']}")

            escolha = st.radio(pergunta["texto"], alternativas, key=f"quiz_{quiz_id}_perg_{pergunta['id']}")

            if st.button("Responder", key=f"resp_{quiz_id}_{pergunta['id']}", use_container_width=True):
                indice_resposta = alternativas.index(escolha)
                retorno = quiz_service.responder_pergunta(participacao_id, pergunta["id"], indice_resposta)

                if retorno["sucesso"]:
                    st.success(retorno["dados"]["feedback"])
                    st.info(f"Sua pontuação: {retorno['dados']['pontuacao']} pontos")
                else:
                    st.error(retorno["mensagem"])

        st.divider()

    quiz_ranking = st.number_input("Quiz Ranking", min_value=1, key="ranking")
    if st.button("Ver Ranking", use_container_width=True):
        _mostrar_ranking(quiz_ranking)


def _mostrar_ranking(quiz_id):
    resultado = quiz_service.obter_ranking(quiz_id)
    if resultado["sucesso"]:
        st.subheader("Ranking")
        for posicao, jogador in enumerate(resultado["dados"], start=1):
            usuario_dados = jogador.get("usuarios") or {}
            nome = usuario_dados.get("nome", "Aluno")
            st.write(f"**{posicao}º lugar** - {nome} - {jogador['pontuacao']} pontos")
    else:
        st.error(resultado["mensagem"])