import streamlit as st


def configurar_acessibilidade():

    if "alto_contraste" not in st.session_state:
        st.session_state["alto_contraste"] = False

    if "tempo_extra" not in st.session_state:
        st.session_state["tempo_extra"] = 0

    st.sidebar.title("Acessibilidade")

    alto_contraste = st.sidebar.checkbox(
        "Alto contraste"
    )

    tempo_extra = st.sidebar.selectbox(
        "Tempo extra por questão",
        [0, 30, 60]
    )

    leitura = st.sidebar.checkbox(
        "Leitura da questão"
    )

    st.session_state[
        "alto_contraste"
    ] = alto_contraste

    st.session_state[
        "tempo_extra"
    ] = tempo_extra

    st.session_state[
        "leitura"
    ] = leitura

    if alto_contraste:

        st.markdown(
            """
            <style>
            .stApp {
                background-color: black;
                color: white;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
