import streamlit as st
from services.desafio_service import listar_desafios
from utils.estilo import aplicar_estilo, cabecalho

# Tentativa segura de importar as funcoes de voto
try:
    from services.votacao_service import listar_votos, registrar_voto
except ImportError:
    try:
        from services.votacao_service import obter_votos as listar_votos, registrar_voto
    except ImportError:
        from services.votacao_service import registrar_voto
        def listar_votos():
            return []


def tela_votacao():
    # Injeta as configuracoes do seu CSS global
    aplicar_estilo()

    usuario = st.session_state.get("usuario_logado", {})
    tipo = usuario.get("tipo_usuario", "aluno")

    cabecalho(
        "Sistema de Votacao",
        "Vote nos melhores projetos ou gerencie as votacoes ativas"
    )

    if tipo == "professor":
        st.subheader("Gerenciamento de Votos")
        
        if st.button("Listar Todos os Votos", width="stretch"):
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
                
    else:
        st.subheader("Pesquisar e Votar")
        
        pesquisa = st.text_input("Pesquisar desafio por titulo")
        desafios = listar_desafios()

        # Filtro de busca por texto que voce criou na versao antiga
        if pesquisa and desafios:
            desafios = [
                d for d in desafios
                if pesquisa.lower() in d.get("titulo", "").lower()
            ]

        if not desafios:
            st.warning("Nenhum desafio encontrado")
            return

        # Renderiza os desafios usando o container com borda estruturado pelo seu CSS
        for desafio in desafios:
            with st.container(border=True):
                st.subheader(desafio.get("titulo", "Sem Titulo"))
                st.write(f"Prazo final: {desafio.get('data_limite', 'Nao informado')}")
                
                # Input para o aluno votar diretamente aqui
                aluno_id = st.number_input(
                    "ID do Aluno Autor do Projeto", 
                    min_value=1, 
                    step=1, 
                    key=f"aluno_id_{desafio.get('id')}"
                )

                if st.button("Confirmar Voto", key=f"voto_{desafio.get('id')}", width="stretch"):
                    if aluno_id == usuario.get("id"):
                        st.error("Voce nao pode votar no seu proprio projeto.")
                    else:
                        resultado = registrar_voto(desafio.get("id"), aluno_id)
                        if isinstance(resultado, dict) and resultado.get("sucesso"):
                            st.success("Seu voto foi registrado com sucesso!")
                        elif isinstance(resultado, dict):
                            st.error(resultado.get("mensagem", "Erro ao registrar voto."))
                        else:
                            st.success("Operacao de votacao concluida.")
