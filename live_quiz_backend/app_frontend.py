import streamlit as st
import live_quiz_backend as lqb
# Configuração da Página
st.set_page_config(page_title="Live Quiz - Painel de Testes", layout="wide")
# Inicializando estado na sessão
if "usuario_id" not in st.session_state:
    st.session_state["usuario_id"] = None
if "tipo_perfil" not in st.session_state:
    st.session_state["tipo_perfil"] = "Professor"
if "quiz_ativo" not in st.session_state:
    st.session_state["quiz_ativo"] = None
st.title("🎯 Live Quiz - Plataforma de Testes")
# --- BARRA LATERAL (LOGIN) ---
with st.sidebar:
    st.header("🔑 Simulação de Login")
    perfil = st.radio("Selecione seu Perfil", ["Professor", "Aluno"])
    user_id = st.number_input("Digite o ID do seu Usuário (banco de dados)", min_value=1, step=1)
    
    if st.button("Fazer Login"):
        st.session_state["usuario_id"] = user_id
        st.session_state["tipo_perfil"] = perfil
        st.success(f"Logado como {perfil} (ID: {user_id})")
# Se não estiver logado, pede para fazer login
if st.session_state["usuario_id"] is None:
    st.info("👈 Por favor, faça o login na barra lateral para acessar o painel correspondente.")
    st.stop()
# ==========================================
# VISÃO DO PROFESSOR
# ==========================================
if st.session_state["tipo_perfil"] == "Professor":
    st.header("👨‍🏫 Painel do Professor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Criar Novo Quiz")
        titulo_quiz = st.text_input("Título do Quiz")
        if st.button("Criar Quiz"):
            res = lqb.criar_quiz(titulo_quiz, st.session_state["usuario_id"])
            if res["sucesso"]:
                st.success(f"Quiz '{titulo_quiz}' criado com sucesso! ID: {res['dados']['id']}")
                st.session_state["quiz_ativo"] = res['dados']['id']
            else:
                st.error(res["mensagem"])
                
        st.subheader("3. Gerenciar Status do Quiz")
        q_id_status = st.number_input("ID do Quiz", min_value=1, step=1, value=st.session_state.get("quiz_ativo") or 1, key="status_qid")
        status_novo = st.selectbox("Novo Status", ["iniciado", "finalizado"])
        if st.button("Atualizar Status"):
            res = lqb.alterar_status_quiz(q_id_status, st.session_state["usuario_id"], status_novo)
            if res["sucesso"]:
                st.success(f"Status atualizado para '{status_novo}' com sucesso!")
            else:
                st.error(res["mensagem"])
                
    with col2:
        st.subheader("2. Adicionar Perguntas")
        q_id = st.number_input("ID do Quiz", min_value=1, step=1, value=st.session_state.get("quiz_ativo") or 1, key="add_qid")
        texto_pergunta = st.text_area("Texto da Pergunta")
        
        # Coletando alternativas
        alts_raw = st.text_input("Alternativas (separadas por vírgula)", placeholder="Ex: Paris, Londres, Madri, Roma")
        alternativas = [a.strip() for a in alts_raw.split(",") if a.strip()]
        
        if alternativas:
            st.write("Alternativas detectadas:", alternativas)
            indice_correto = st.selectbox("Selecione a alternativa correta", range(len(alternativas)), format_func=lambda i: alternativas[i])
        else:
            indice_correto = 0
            
        if st.button("Adicionar Pergunta"):
            res = lqb.adicionar_pergunta(q_id, st.session_state["usuario_id"], texto_pergunta, alternativas, indice_correto)
            if res["sucesso"]:
                st.success("Pergunta adicionada!")
            else:
                st.error(res["mensagem"])
    st.divider()
    st.subheader("🏆 Acompanhar Ranking em Tempo Real")
    quiz_rank_prof = st.number_input("ID do Quiz para ver ranking", min_value=1, step=1, value=st.session_state.get("quiz_ativo") or 1, key="rank_qid_prof")
    if st.button("Atualizar Ranking", key="btn_rank_prof"):
        res = lqb.obter_ranking(quiz_rank_prof)
        if res["sucesso"] and res["dados"]:
            st.table(res["dados"])
        else:
            st.info("Nenhuma participação encontrada ou erro ao carregar.")
# ==========================================
# VISÃO DO ALUNO
# ==========================================
elif st.session_state["tipo_perfil"] == "Aluno":
    st.header("🎓 Painel do Aluno")
    
    st.subheader("1. Entrar no Quiz")
    colA, colB = st.columns([2, 1])
    with colA:
        quiz_id_aluno = st.number_input("Digite o ID do Quiz que deseja participar", min_value=1, step=1)
    with colB:
        st.write("") # Spacer
        st.write("")
        if st.button("Entrar"):
            res = lqb.entrar_quiz(st.session_state["usuario_id"], quiz_id_aluno)
            if res["sucesso"]:
                st.success("Você ingressou no Quiz com sucesso!")
                if "participacao_id" not in st.session_state or st.session_state["participacao_id"] != res["dados"]["id"]:
                    st.session_state["participacao_id"] = res["dados"]["id"]
            else:
                st.error(res["mensagem"])
    st.divider()
    
    st.subheader("2. Responder Pergunta")
    if "participacao_id" in st.session_state:
        st.info(f"Sua Participação Atual: ID {st.session_state['participacao_id']}")
        
        # Buscar perguntas do quiz
        res_perguntas = lqb.obter_perguntas_quiz(quiz_id_aluno)
        
        if res_perguntas["sucesso"] and res_perguntas["dados"]:
            perguntas = res_perguntas["dados"]
            
            # Exibir dropdown com as perguntas disponíveis
            opcoes_perguntas = {p["id"]: f"Pergunta {p['id']}: {p['texto']}" for p in perguntas}
            pergunta_id_responder = st.selectbox(
                "Selecione a Pergunta", 
                options=list(opcoes_perguntas.keys()), 
                format_func=lambda x: opcoes_perguntas[x]
            )
            
            # Identificar alternativas da pergunta selecionada
            pergunta_selecionada = next(p for p in perguntas if p["id"] == pergunta_id_responder)
            alternativas = pergunta_selecionada.get("alternativas", [])
            
            if alternativas:
                # Exibir as alternativas como Radio Buttons
                resposta_indice = st.radio("Qual a sua resposta?", range(len(alternativas)), format_func=lambda i: alternativas[i])
                
                if st.button("Enviar Resposta!"):
                    res = lqb.responder_pergunta(st.session_state["participacao_id"], pergunta_id_responder, resposta_indice)
                    if res["sucesso"]:
                        if res["dados"]["correta"]:
                            st.success("🎉 ACERTOU! " + res["dados"]["feedback"])
                        else:
                            st.error("❌ ERROU! " + res["dados"]["feedback"])
                    else:
                        st.error(res["mensagem"])
            else:
                st.warning("Esta pergunta não possui alternativas configuradas.")
        else:
            st.warning("O professor ainda não adicionou perguntas a este quiz ou ocorreu um erro.")
            
    else:
        st.warning("Entre em um quiz primeiro para poder responder perguntas.")
    st.divider()
    
    st.subheader("🏆 Ver Ranking (Fim de Jogo)")
    if st.button("Mostrar Ranking Geral", key="btn_rank_aluno"):
        res = lqb.obter_ranking(quiz_id_aluno)
        if res["sucesso"] and res["dados"]:
            st.table(res["dados"])
        else:
            st.info("Ranking indisponível no momento.")
