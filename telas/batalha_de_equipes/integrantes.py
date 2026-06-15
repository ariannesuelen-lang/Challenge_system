# telas/batalha_de_equipes/integrantes.py
import streamlit as st
from services import batalha_service
from utils.estilo import aplicar_estilo, cabecalho


def _safe_dict(v):
    return v if isinstance(v, dict) else {}


def _safe_list(v):
    return v if isinstance(v, list) else []


def tela_batalha_integrantes():

    aplicar_estilo()

    usuario = st.session_state.usuario_logado
    tipo    = usuario.get("tipo_usuario", "aluno")
    user_id = usuario.get("id")

    cabecalho("Integrantes dos Times", "Veja e gerencie os membros de cada time")

    if st.button("Voltar"):
        st.session_state.pagina = "batalha_de_equipes"
        st.rerun()

    st.divider()

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        st.error("Sessão inválida.")
        return

    # --------------------------------------------------
    # VISÃO DO PROFESSOR (GERENCIAMENTO GLOBAL)
    # --------------------------------------------------
    if tipo == "professor":
        times = batalha_service.listar_times()
        if not times:
            st.warning("Nenhum time cadastrado.")
            return

        mapa_times_geral = {
            t.get("nome"): t.get("id")
            for t in times
            if isinstance(t, dict) and t.get("nome") and t.get("id")
        }

        nome_time_sel = st.selectbox("Selecione o Time para gerenciar", list(mapa_times_geral.keys()))
        time_id = mapa_times_geral[nome_time_sel]

        # Busca os membros do time selecionado através do serviço unificado
        membros = batalha_service.listar_membros_time(time_id)

        st.markdown(f"#### Membros atuais do {nome_time_sel}")
        if not membros:
            st.info("Este time ainda não possui membros.")
        else:
            for m in membros:
                st.write(f"- {m.get('nome')} ({m.get('email')})")

        st.divider()

        # Aba de Adicionar Aluno
        with st.expander("Adicionar Aluno ao Time", expanded=False):
            todos_alunos = batalha_service.listar_alunos()
            
            # Filtra alunos que já possuem um time para evitar duplicidade na listagem visual
            alunos_disponiveis = []
            for a in todos_alunos:
                if isinstance(a, dict) and a.get("id") and a.get("nome"):
                    if not batalha_service.aluno_tem_time(a["id"]):
                        alunos_disponiveis.append(a)

            mapa_add = {
                al.get("nome"): al.get("id") for al in alunos_disponiveis
            }

            if mapa_add:
                sel_add = st.selectbox("Aluno disponível", list(mapa_add.keys()), key="add_aluno")
                if st.button("Adicionar", use_container_width=True):
                    batalha_service.adicionar_aluno(time_id, mapa_add[sel_add])
                    st.success("Aluno adicionado com sucesso!")
                    st.rerun()
            else:
                st.info("Todos os alunos cadastrados já possuem um time.")

        # Aba de Remover Aluno
        with st.expander("Remover Aluno do Time", expanded=False):
            mapa_rm = {
                m.get("nome"): m.get("id")
                for m in membros
                if isinstance(m, dict) and m.get("nome") and m.get("id")
            }
            if mapa_rm:
                sel_rm = st.selectbox("Membro", list(mapa_rm.keys()), key="rm_aluno")
                if st.button("Remover", use_container_width=True):
                    batalha_service.remover_aluno(time_id, mapa_rm[sel_rm])
                    st.success("Membro removido.")
                    st.rerun()
            else:
                st.info("Nenhum membro para remover.")

        st.divider()

        # Aba de Mover Aluno de Grupo
        with st.expander("Mover aluno para outro time", expanded=False):
            mapa_mv = {
                m.get("nome"): m.get("id")
                for m in membros
                if isinstance(m, dict) and m.get("nome") and m.get("id")
            }
            if mapa_mv and mapa_times_geral:
                col3, col4 = st.columns(2)
                with col3:
                    aluno_mv = st.selectbox("Aluno", list(mapa_mv.keys()), key="mover_aluno")
                with col4:
                    # Filtra o próprio time atual para não aparecer no destino de transferência
                    destinos_filtrados = {k: v for k, v in mapa_times_geral.items() if v != time_id}
                    destino = st.selectbox("Time de Destino", list(destinos_filtrados.keys()), key="destino_time")
                
                if st.button("Transferir Aluno", use_container_width=True):
                    batalha_service.mover_aluno(mapa_mv[aluno_mv], destinos_filtrados[destino])
                    st.success("Aluno transferido de equipe!")
                    st.rerun()
            else:
                st.info("Nenhum membro disponível neste time para transferir.")

    # --------------------------------------------------
    # VISÃO DO ALUNO (CONSULTA DO PRÓPRIO TIME)
    # --------------------------------------------------
    else:
        # 🛠️ CORREÇÃO CRÍTICA: Substituído o supabase.table bruto pelo método do Repositório via Service
        time_id_estudante = batalha_service.obter_time_do_aluno(user_id)

        if not time_id_estudante:
            st.warning("Você ainda não está associado a nenhum time. Vá até a aba 'Times' e escolha uma equipe.")
            return

        # Puxa a listagem completa para achar o nome textual do time dele
        todos_os_times = batalha_service.listar_times()
        registro_time = next((t for t in todos_os_times if t.get("id") == time_id_estudante), None)
        nome_time_estudante = registro_time.get("nome", "Seu Time") if registro_time else "Seu Time"

        st.markdown(f"### 🛡️ Equipe: **{nome_time_estudante}**")
        st.write("Abaixo estão os seus colegas de equipe cadastrados na plataforma:")

        # Lista os parceiros de grupo utilizando a inteligência do monólito
        colegas = batalha_service.listar_membros_time(time_id_estudante)

        if colegas:
            for c in colegas:
                # Destaca se o nome listado for o do próprio usuário logado
                if c.get("id") == user_id:
                    st.write(f"- **{c.get('nome')} (Você)** — *{c.get('email')}*")
                else:
                    st.write(f"- {c.get('nome')} — *{c.get('email')}*")
        else:
            st.info("Não foi possível carregar os integrantes do seu time.")