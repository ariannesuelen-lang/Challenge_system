import streamlit as st


def aplicar_alto_contraste():

    if st.session_state.get(
        "alto_contraste"
    ):

        st.markdown(
            """
            <style>

            .stApp {
                background-color: black;
                color: white;
            }

            button {
                background-color: white !important;
                color: black !important;
            }

            </style>
            """,
            unsafe_allow_html=True
        )
