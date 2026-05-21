import streamlit as st
from modules import lista, votacao, visualizar, editar, admin_desafios

st.set_page_config(page_title="Votação de Desafios", layout="centered")

# Estado global
defaults = {
    'pagina': 'lista',
    'voto_id': None,
    'desafio': None,
    'id_usuario': 'user_123',
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Header
col1, col2 = st.columns([4, 1])
with col2:
    st.markdown("👤 *Aluno*")
st.divider()

def carregar_css():
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

carregar_css()
st.markdown("""
    <div style="
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 20px;
        background: #111210;
        border-radius: 10px;
        border: 0.5px solid #2C2C2A;
        margin-bottom: 1.5rem;
    ">
        <span style="font-size:15px; font-weight:500; color:#D3D1C7;">
            <span style="color:#5DCAA5">●</span> Votação de Desafios
        </span>
        <span style="font-size:12px; background:#1D1D1B; border:0.5px solid #2C2C2A;
                     color:#888780; padding:4px 12px; border-radius:999px;">
            Aluno
        </span>
    </div>
""", unsafe_allow_html=True)

# Roteador
paginas = {
    'lista': lista.render,
    'votacao': votacao.render,
    'visualizar': visualizar.render,
    'editar': editar.render,
    'admin_desafios': admin_desafios.render
}

paginas[st.session_state.pagina]()