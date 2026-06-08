import streamlit as st
from services.desafio_service import listar_desafios
from utils.estilo import aplicar_estilo, cabecalho

# Tentativa segura de importar as funcoes de voto do service
try:
    from services.votacao_service import listar_votos, registrar_voto
except ImportError:
    try:
        from services.votacao_service import obter_votos as listar_votos, registrar_voto
    except ImportError:
        try:
            from services.votacao_service import get_votos as listar_votos, registrar_voto
        except ImportError:
            from services.votacao_service import registrar_voto
            def listar_votos():
                return []


def tela_votacao():
    # Injeta as configuracoes do seu CSS global (Navbar e botoes)
    aplicar_estilo()

    usuario = st.session_state.get("usuario_logado", {})
    tipo = usuario.get("tipo_usuario", "aluno")
    usuario_id_logado = usuario.get("id")

    cabecalho(
        "Sistema de Votacao",
        "Vote nos melhores projetos ou gerencie as votacoes ativas"
    )

    if tipo == "professor":
        st.subheader("Gerenciamento de Votos")
        
        if st.button("Listar Todos os Votos", width="stretch"):
            try:
                votos = listar_votos()
                if votos:
                    for v in votos:
                        st.markdown(f"""
                        <div style="
                            background: #f0f9ff;
                            border-left: 4px solid #1b3a5c;
                            border-radius: 8px;
                            padding: 12px 16px;
                            margin-bottom: 8px;
                        ">
                            <span style="color: #0d1b2a; font-weight: 600;">Desafio ID: {v.get('desafio_id', '-')}</span><br>
                            <span style="color: #555; font-size: 13px;">Aluno ID: {v.get('aluno_id', '-')} | Votos: {v.get('votos', 0)}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("Nenhum voto registrado ate o momento.")
            except Exception:
                st.error("Erro ao listar votos do banco de dados. Verifique a tabela no Supabase.")
                
    else:
        st.subheader("Pesquisar e Votar")
