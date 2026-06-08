import streamlit as st

def aplicar_estilo():
    """
    Injeta o CSS customizado para corrigir a legibilidade da barra lateral
    e dos botoes do menu contra o fundo escuro.
    """
    st.markdown("""
        <style>
            /* 1. GARANTE O FUNDO ESCURO DA NAVBAR LATERAL */
            [data-testid="stSidebar"] {
                background-color: #0d1b2a !important;
            }

            /* 2. FORÇA TEXTOS, PARÁGRAFOS E TEXTOS DE LINKS PARA BRANCO */
            [data-testid="stSidebar"] .stMarkdown p,
            [data-testid="stSidebar"] span,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] a {
                color: #ffffff !important;
                text-decoration: none !important;
            }

            /* 3. ESTILIZA OS BOTÕES DO MENU (ST.BUTTON) DENTRO DA NAVBAR */
            [data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"] {
                background-color: #1b3a5c !important;
                color: #ffffff !important;
                border: 1px solid #00b4d8 !important;
                border-radius: 6px !important;
                transition: all 0.3s ease;
                width: 100% !important;
                display: block !important;
            }

            /* 4. EFEITO HOVER - COR DO BOTÃO AO PASSAR O MOUSE (INVERTE PARA CONTRASTE) */
            [data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]:hover {
                background-color: #00b4d8 !important;
                color: #0d1b2a !important;
                border-color: #ffffff !important;
                cursor: pointer;
            }

            /* 5. GARANTE QUE OS TEXTOS DE DENTRO DOS BOTÕES FIQUEM BRANCOS POR PADRÃO */
            [data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"] p {
                color: #ffffff !important;
            }

            /* CORREÇÃO DO TEXTO DO BOTÃO NO HOVER */
            [data-testid="stSidebar"] button[data-testid="stBaseButton-secondary"]:hover p {
                color: #0d1b2a !important;
            }
        </style>
    """, unsafe_allow_html=True)


def cabecalho(titulo, subtitulo=""):
    """
    Gera um bloco de titulo estilizado para o topo das paginas centrais.
    """
    st.markdown(f"""
        <div style="
            background: #1b3a5c; 
            padding: 20px; 
            border-radius: 10px; 
            margin-bottom: 25px;
            border-left: 5px solid #00b4d8;
        ">
            <h2 style="color: white; margin: 0; padding: 0;">{titulo}</h2>
            {f'<p style="color: #a5f3fc; margin: 5px 0 0 0; font-size: 14px;">{subtitulo}</p>' if subtitulo else ''}
        </div>
    """, unsafe_allow_html=True)
