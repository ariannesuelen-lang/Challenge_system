import streamlit as st
from services.desafio_service import listar_desafios

def tela_home():

    usuario = st.session_state.usuario_logado
    desafio = listar_desafios()
    
    st.write(st.session_state.usuario_logado)
    
    st.title(
        f"Bem-vindo(a), {usuario['nome']}"
    )

    st.divider()

    st.subheader(
        "Desafios disponíveis"
    )
    desafios = listar_desafios()

    if desafios:

        for desafio in desafios[:5]:
            with st.container(border=True):
                st.write(
                    f" {desafio['titulo']}"
                )

                st.caption(
                    f"Nível: {desafio['nivel']}"
                )

                st.write(
                    desafio['descricao']
                )

                st.write(
                    f"Prazo: {desafio['data_limite']}"
                )

    else:

        if desafios:

            for desafio in desafios[:5]:
                st.write(
                    f"🗳️ {desafio['titulo']}"
                )

        else:

            st.info(
                "Nenhum desafio disponível para voto"
            )
    st.divider()
#Votação
    st.subheader(
        "Votação disponíveis"
    )

    if desafios:

        for desafio in desafios[:5]:
            st.write(
                f" {desafio['titulo']}"
            )

    else:

        st.info(
            "Nenhum desafio disponível para voto"
        )

    st.divider()

    st.subheader(
        "Mini-provas"
    )

    st.warning(
        "Sistema em construção"
    )


    st.divider()

    st.subheader(
        "Quiz ao Vivo"
    )

    st.warning(
        "Sistema em construção"
    )

    st.divider()

    st.subheader(
        "Batalha de Equipes"
    )

    st.warning(
        "Sistema em construção"
    )
