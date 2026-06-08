import streamlit as st
from services.desafio_service import listar_desafios
from utils.estilo import aplicar_estilo, cabecalho


def tela_home():
    aplicar_estilo()

    usuario = st.session_state.get("usuario_logado", {})
    
    # Proteção para garantir que o app não quebre se o objeto usuário estiver incompleto
    nome_usuario = usuario.get("nome") or usuario.get("username") or "Usuário"
    tipo_usuario = usuario.get("tipo_usuario") or usuario.get("perfil") or "aluno"

    cabecalho(
        f"Bem-vindo(a), {nome_usuario}",
        f"Perfil: {tipo_usuario.capitalize()}"
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.write("### O que é o Challenge System?")
        st.write(
            "Uma plataforma gamificada para resolver desafios, participar de mini-provas, "
            "votar nos melhores projetos e competir em equipes!"
        )
        st.write("Utilize o menu lateral para navegar entre as funcionalidades.")

    with col2:
        desafios = listar_desafios()
        if desafios:
            st.write("### Últimos Desafios")
            for desafio in desafios[:3]:
                st.write(f"**{desafio.get('titulo', 'Sem Título')}**")
                
                # Busca segura para o nível de dificuldade (evita o KeyError)
                nivel = desafio.get('nivel_dificuldade') or desafio.get('nivel') or '-'
                st.caption(f"Nível: {nivel}")
                
                st.write(desafio.get('descricao', ''))
                st.markdown("---")
        else:
            st.info("Nenhum desafio encontrado.")
