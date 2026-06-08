def aplicar_estilo():
    import streamlit as st
    st.markdown("""
    <style>
        /* =========================================
           PALETA
           --azul-escuro : #0d1b2a
           --azul-medio  : #1b3a5c
           --ciano       : #00b4d8
           --ciano-hover : #0096c7
           --fundo-card  : #f0f9ff
           --texto-card  : #0d1b2a
           --texto-sub   : #555555
        ========================================= */

        /* ----- FUNDO PRINCIPAL ----- */
        .stApp {
            background-color: #ffffff !important;
        }

        /* ----- SIDEBAR ----- */
        [data-testid="stSidebar"] {
            background-color: #0d1b2a !important;
        }
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] *,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] div {
            color: #0d1b2a !important;
        }

        /* ----- TITULOS NO CONTEUDO PRINCIPAL ----- */
        .stApp h1,
        .stApp h2,
        .stApp h3 {
            color: #0d1b2a !important;
        }

        /* Garantir que titulos dentro de cards HTML fiquem corretos */
        .stApp [data-testid="stMarkdownContainer"] h1,
        .stApp [data-testid="stMarkdownContainer"] h2,
        .stApp [data-testid="stMarkdownContainer"] h3 {
            color: #ffffff !important;
        }

        /* ----- TEXTO GERAL NO CONTEUDO ----- */
        .stApp [data-testid="stMarkdownContainer"] p,
        .stApp [data-testid="stMarkdownContainer"] span,
        .stApp .stText,
        .stApp label {
            color: #ffffff !important;
        }

        /* ----- BOTOES GLOBAIS (ciano) ----- */
        .stButton > button {
            background-color: #00b4d8 !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 8px 20px !important;
            transition: background 0.2s !important;
        }
        .stButton > button:hover {
            background-color: #0096c7 !important;
            color: #ffffff !important;
        }
        .stButton > button:focus,
        .stButton > button:active {
            background-color: #0096c7 !important;
            color: #ffffff !important;
            box-shadow: none !important;
        }

        /* ----- BOTOES NA SIDEBAR (sobrescreve para transparente) ----- */
        [data-testid="stSidebar"] .stButton > button {
            background-color: transparent !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            width: 100% !important;
            text-align: left !important;
            padding: 0.5rem 1rem !important;
            transition: background 0.2s !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background-color: #00b4d8 !important;
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] .botao-ativo .stButton > button {
            background-color: #00b4d8 !important;
            color: #ffffff !important;
            border-left: 4px solid #ffffff !important;
            font-size: 1.05rem !important;
            padding-left: 0.85rem !important;
        }

        /* ----- INPUTS ----- */
        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox select {
            border: 1.5px solid #00b4d8 !important;
            border-radius: 8px !important;
            color: #0d1b2a !important;
            background-color: #ffffff !important;
        }
        .stTextInput input:focus,
        .stTextArea textarea:focus {
            border-color: #0096c7 !important;
            box-shadow: 0 0 0 2px rgba(0,180,216,0.2) !important;
        }

        /* Labels dos inputs */
        .stTextInput label,
        .stTextArea label,
        .stSelectbox label,
        .stNumberInput label,
        .stSlider label,
        .stDateInput label,
        .stCheckbox label,
        .stRadio label {
            color: #0d1b2a !important;
            font-weight: 500 !important;
        }

        /* ----- SELECTBOX ----- */
        [data-testid="stSelectbox"] > div > div {
            border: 1.5px solid #00b4d8 !important;
            border-radius: 8px !important;
        }

        /* ----- CONTAINERS COM BORDA ----- */
        [data-testid="stVerticalBlock"] > div:has(> [data-testid="stVerticalBlockBorderWrapper"]) {
            border: 1.5px solid #00b4d8 !important;
            border-radius: 10px !important;
        }

        /* ----- DIVIDER ----- */
        hr {
            border-top: 2px solid #00b4d8 !important;
        }

        /* ----- METRIC ----- */
        [data-testid="stMetric"] {
            background: #f0f9ff !important;
            border-radius: 8px !important;
            border-left: 4px solid #00b4d8 !important;
            padding: 8px 12px !important;
        }
        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"],
        [data-testid="stMetricDelta"] {
            color: #0d1b2a !important;
        }

        /* ----- EXPANDER ----- */
        details {
            border: 1px solid #00b4d8 !important;
            border-radius: 8px !important;
            padding: 4px 8px !important;
        }
        details summary,
        details summary p {
            color: #0d1b2a !important;
            font-weight: 600 !important;
        }

        /* ----- TABS ----- */
        [data-testid="stTabs"] [data-baseweb="tab"] {
            color: #0d1b2a !important;
        }
        [data-testid="stTabs"] [aria-selected="true"] {
            color: #00b4d8 !important;
            border-bottom: 2px solid #00b4d8 !important;
        }

        /* ----- DATAFRAME ----- */
        [data-testid="stDataFrame"] {
            border: 1px solid #00b4d8 !important;
            border-radius: 8px !important;
        }

        /* ----- ALERTAS ----- */
        [data-testid="stAlert"] {
            border-radius: 8px !important;
        }

        /* ----- MODO ESCURO: sobrescreve fundo e texto ----- */
        @media (prefers-color-scheme: dark) {
            .stApp {
                background-color: #0a0f1a !important;
            }
            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp [data-testid="stMarkdownContainer"] p,
            .stApp [data-testid="stMarkdownContainer"] span,
            .stApp label,
            .stTextInput label,
            .stTextArea label,
            .stSelectbox label,
            .stNumberInput label,
            .stSlider label,
            .stDateInput label,
            .stCheckbox label,
            .stRadio label,
            details summary,
            details summary p,
            [data-testid="stMetricLabel"],
            [data-testid="stMetricValue"],
            [data-testid="stTabs"] [data-baseweb="tab"] {
                color: #e8f4fd !important;
            }
            .stTextInput input,
            .stTextArea textarea {
                background-color: #1a2535 !important;
                color: #e8f4fd !important;
            }
            [data-testid="stMetric"] {
                background: #1a2535 !important;
            }
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


def info_box(texto, cor_borda="#00b4d8", cor_fundo="#f0f9ff", cor_texto="#0d1b2a"):
    """Caixa de informacao padronizada."""
    import streamlit as st
    st.markdown(f"""
    <div style="
        background:{cor_fundo};
        border-left:4px solid {cor_borda};
        border-radius:8px;
        padding:14px 18px;
        margin-bottom:10px;
    ">
        <span style="color:{cor_texto};">{texto}</span>
    </div>
    """, unsafe_allow_html=True)
