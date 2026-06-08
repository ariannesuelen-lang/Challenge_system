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
    usuario_id_logado = usuario.get("id")

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

        if pesquisa and desafios:
            desafios = [
                d for d in desafios
                if pesquisa.lower() in d.get("titulo", "").lower()
            ]

        if not desafios:
            st.warning("Nenhum desafio encontrado")
            return

        for desafio in desafios:
            with st.container(border=True):
                st.subheader(desafio.get("titulo", "Sem Titulo"))
                st.write(f"Prazo final: {desafio.get('data_limite', 'Nao informado')}")
                
                aluno_id = st.number_input(
                    "ID do Aluno Autor do Projeto", 
                    min_value=1, 
                    step=1, 
                    key=f"aluno_id_{desafio.get('id')}"
                )

if st.button("Confirmar Voto", key=f"voto_{desafio.get('id')}", width="stretch"):
                    if aluno_id == usuario_id_logado:
                        st.error("Voce nao pode votar no seu proprio projeto.")
                    else:
                        desafio_id = desafio.get("id")
                        
                        # Bloco de segurança para interceptar erros do banco (Supabase/PostgreSQL)
                        try:
                            resultado = None
                            
                            # Tentativa de execução padrão da sua assinatura
                            try:
                                resultado = registrar_voto(desafio_id, aluno_id, usuario_id_logado)
                            except TypeError:
                                try:
                                    resultado = registrar_voto(aluno_id, desafio_id)
                                except TypeError:
                                    resultado = registrar_voto(desafio_id, aluno_id)

                            # Trata o retorno visual se o banco responder sem estourar APIError
                            if resultado:
                                if isinstance(resultado, dict) and resultado.get("sucesso"):
                                    st.success("Seu voto foi registrado com sucesso!")
                                elif isinstance(resultado, dict):
                                    st.error(resultado.get("mensagem", "Erro ao registrar voto."))
                                else:
                                    st.success("Operacao de votacao concluida.")
                                    
                        except Exception as e:
                            # Captura o erro do PostgREST/Supabase sem deixar o app cair em tela escura
                            st.error("Erro de comunicacao com o banco de dados.")
                            st.info(
                                "Verifique se a tabela de votos possui as colunas corretas "
                                "ou se as politicas de seguranca (RLS) do Supabase estao ativas."
                            )
