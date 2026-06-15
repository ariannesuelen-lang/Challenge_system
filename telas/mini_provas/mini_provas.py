# telas/mini_provas/mini_provas.py
import streamlit as st
# 🌟 ALTERADO: Puxando a instância única global do serviço
from services import mini_prova_service
from utils.estilo import aplicar_estilo, cabecalho


def tela_mini_provas():
    aplicar_estilo()

    if "alto_contraste" not in st.session_state:
        st.session_state.alto_contraste = False

    usuario = st.session_state.usuario_logado

    cabecalho("Mini-provas", "Realize as provas disponíveis")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Minha Pontuação", use_container_width=True):
            st.session_state.pagina = "pontuacao_mini_provas"
            st.rerun()

    with col2:
        if st.button("Desempenho", use_container_width=True):
            st.session_state.pagina = "desempenho_mini_provas"
            st.rerun()

    with col3:
        with st.popover("Acessibilidade"):
            alto = st.checkbox("Alto contraste", value=st.session_state.alto_contraste)
            st.session_state.alto_contraste = alto
            st.checkbox("Leitura por questão")
            st.divider()
            st.subheader("Solicitar tempo extra")
            
            # 🌟 ALTERADO: Chamada via método da classe de serviço
            mini_provas_lista = mini_prova_service.listar_mini_provas()
            nomes = [p["titulo"] for p in mini_provas_lista] if mini_provas_lista else ["Nenhuma prova disponível"]
            st.selectbox("Mini prova", nomes)
            st.text_area("Justificativa")
            if st.button("Enviar solicitação"):
                st.success("Solicitação enviada")

    if st.session_state.alto_contraste:
        st.markdown("""
        <style>
            .stApp { background-color: #000000 !important; }
            .stApp * { color: #ffffff !important; }
        </style>
        """, unsafe_allow_html=True)

    st.divider()
    pesquisa = st.text_input("Pesquisar mini prova")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Mini Provas Disponíveis")
    with col2:
        if st.button("Resultados", use_container_width=True):
            st.session_state.pagina = "historico_provas"
            st.rerun()

    # 🌟 ALTERADO: Listagem usando o serviço centralizado
    mini_provas = mini_prova_service.listar_mini_provas()

    if pesquisa:
        mini_provas = [p for p in mini_provas if pesquisa.lower() in p.get("titulo", "").lower()]

    if not mini_provas:
        st.info("Nenhuma mini prova disponível.")
        return

    for prova in mini_provas:
        st.markdown(f"""
        <div style="
            background:#f0f9ff;
            border-left:4px solid #00b4d8;
            border-radius:8px;
            padding:14px 18px;
            margin-bottom:10px;
        ">
            <strong style="color:#0d1b2a; font-size:15px;">{prova.get('titulo', 'Sem título')}</strong><br>
            <span style="color:#555; font-size:13px;">{prova.get('descricao','Sem descrição cadastrada.')}</span><br>
            <span style="color:#00b4d8; font-size:12px;">Criada em: {prova.get('criado_em','-')}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Fazer prova", key=f"fazer_{prova['id']}", use_container_width=False):
            st.session_state.id_mini_prova = prova["id"]
            st.session_state.pagina = "realizar_mini_prova"
            st.rerun()