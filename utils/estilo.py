def aplicar_estilo():
    import streamlit as st
    st.markdown("""
    <style>
        /* Fundo branco */
        .stApp { background-color: #ffffff; }

        /* Sidebar azul escuro */
        [data-testid="stSidebar"] {
            background-color: #0d1b2a !important;
        }
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        /* Botoes ciano */
        .stButton > button {
            background-color: #00b4d8;
            color: #ffffff;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            padding: 8px 20px;
            transition: background 0.2s;
        }
        .stButton > button:hover {
            background-color: #0096c7;
            color: #ffffff;
        }

        /* Titulos azul escuro */
        h1, h2, h3 {
            color: #0d1b2a !important;
        }

        /* Inputs */
        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox select {
            border: 1.5px solid #00b4d8;
            border-radius: 8px;
        }

        /* Containers com borda ciano */
        [data-testid="stVerticalBlock"] > div:has(> [data-testid="stVerticalBlockBorderWrapper"]) {
            border: 1.5px solid #00b4d8 !important;
            border-radius: 10px !important;
        }

        /* Divider ciano */
        hr { border-top: 2px solid #00b4d8; }

        /* Metric */
        [data-testid="stMetric"] {
            background: #f0f9ff;
            border-radius: 8px;
            border-left: 4px solid #00b4d8;
            padding: 8px 12px;
        }

        /* Expander */
        details {
            border: 1px solid #00b4d8;
            border-radius: 8px;
            padding: 4px 8px;
        }
    </style>
    """, unsafe_allow_html=True)


def card(titulo, subtitulo="", cor_borda="#00b4d8"):
    import streamlit as st
    st.markdown(f"""
    <div style="
        background:#f0f9ff;
        border-left: 4px solid {cor_borda};
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
    ">
        <h3 style="color:#0d1b2a; margin:0;">{titulo}</h3>
        {"<p style='color:#555; margin:4px 0 0;'>" + subtitulo + "</p>" if subtitulo else ""}
    </div>
    """, unsafe_allow_html=True)


def cabecalho(titulo, subtitulo=""):
    import streamlit as st
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #0d1b2a, #1b3a5c);
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 20px;
        border-left: 5px solid #00b4d8;
    ">
        <h1 style="color:#ffffff; margin:0; font-size:26px;">{titulo}</h1>
        {"<p style='color:#90caf9; margin:6px 0 0;'>" + subtitulo + "</p>" if subtitulo else ""}
    </div>
    """, unsafe_allow_html=True)


def badge(texto, cor="#00b4d8"):
    import streamlit as st
    st.markdown(f"""
    <span style="
        background:{cor};
        color:#fff;
        padding:3px 10px;
        border-radius:20px;
        font-size:12px;
        font-weight:600;
    ">{texto}</span>
    """, unsafe_allow_html=True)
