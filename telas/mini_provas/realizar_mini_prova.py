import streamlit as st

from services.mini_prova_service import (
    sortear_questoes,
    finalizar_tentativa
)


def tela_realizar_mini_prova():

    if "mini_prova" not in st.session_state:

        st.warning(
            "Nenhuma mini prova selecionada"
        )

        return

    mini_prova = st.session_state[
        "mini_prova"
    ]

    if "questoes" not in st.session_state:

        st.session_state[
            "questoes"
        ] = sortear_questoes(mini_prova)

    if "indice_questao" not in st.session_state:

        st.session_state[
            "indice_questao"
        ] = 0

    if "respostas" not in st.session_state:

        st.session_state[
            "respostas"
        ] = []

    indice = st.session_state[
        "indice_questao"
    ]

    questoes = st.session_state[
        "questoes"
    ]

    if indice >= len(questoes):

        resultado = finalizar_tentativa(
            st.session_state["respostas"],
            questoes,
            mini_prova,
            1
        )

        st.success("Mini prova finalizada")

        st.write(
            f"Nota: {resultado['nota']}"
        )

        st.write(
            f"Pontuação: {resultado['pontuacao']}"
        )

        return

    questao = questoes[indice]

    st.title(
        f"Questão {indice + 1}"
    )

    st.write(questao["pergunta"])

    resposta = st.radio(
        "Selecione:",
        ["a", "b", "c", "d", "e"],
        format_func=lambda x: {
            "a": questao["alternativa_a"],
            "b": questao["alternativa_b"],
            "c": questao["alternativa_c"],
            "d": questao["alternativa_d"],
            "e": questao["alternativa_e"]
        }[x]
    )

    if st.button("Responder"):

        st.session_state[
            "respostas"
        ].append({
            "pergunta_id": questao["id"],
            "resposta": resposta
        })

        st.session_state[
            "indice_questao"
        ] += 1

        st.rerun()
