import streamlit as st
from database.conexao import supabase
from services.batalha_de_equipes_service import (
    listar_times, listar_membros_time, listar_alunos,
    adicionar_aluno, remover_aluno, mover_aluno
)
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
        st.error("Sessao invalida.")
        return

    if tipo == "professor":
        times = listar_times()
        if not times:
            st.warning("Nenhum time cadastrado.")
            return
        mapa = {
            t.get("nome"): t.get("id")
            for t in times
            if isinstance(t, dict) and t.get("nome") and t.get("id")
        }
        if not mapa:
            st.warning("Times com dados invalidos.")
            return
        sel     = st.selectbox("Selecione o time", list(mapa.keys()))
        time_id = mapa[sel]

    else:
        res  = supabase.table("time_membros") \
            .select("time_id, times(id,nome)") \
            .eq("usuario_id", user_id) \
            .execute()
        data = _safe_list(getattr(res, "data", None))

        if not data:
            st.markdown("""
            <div style="
                background:#fff3e0;
                border-left:4px solid #0d1b2a;
                border-radius:8px;
                padding:14px 18px;
            ">
                <strong style="color:#0d1b2a;">Voce nao participa de nenhum time ainda.</strong>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Entrar em um time"):
                st.session_state.pagina = "batalha_times"
                st.rerun()
            return

        first_row = _safe_dict(data[0])
        time_info = first_row.get("times")
        if isinstance(time_info, list):
            time_info = time_info[0] if time_info else {}
        time_info = _safe_dict(time_info)

        if not time_info.get("id") or not time_info.get("nome"):
            st.error("Erro ao carregar time.")
            return

        time_id = time_info["id"]
        st.markdown(f"""
        <div style="
            background:#e0f7fa;
            border-left:4px solid #00b4d8;
            border-radius:8px;
            padding:12px 16px;
            margin-bottom:12px;
        ">
            <strong style="color:#0d1b2a;">Seu time: {time_info['nome']}</strong>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Membros")

    membros = listar_membros_time(time_id)

    if not membros:
        st.info("Nenhum membro neste time.")
    else:
        st.dataframe(
            membros,
            column_config={
                "id":    st.column_config.NumberColumn("ID"),
                "nome":  st.column_config.TextColumn("Nome"),
                "email": st.column_config.TextColumn("E-mail"),
            },
            use_container_width=True,
            hide_index=True
        )

    if tipo != "professor":
        return

    st.divider()
    st.markdown("### Gestao de membros")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("**Adicionar aluno**")
            alunos   = listar_alunos()
            mapa_add = {
                a.get("nome"): a.get("id")
                for a in alunos
                if isinstance(a, dict) and a.get("nome") and a.get("id")
            }
            if mapa_add:
                sel_add = st.selectbox("Aluno", list(mapa_add.keys()), key="add_aluno")
                if st.button("Adicionar", use_container_width=True):
                    if adicionar_aluno(time_id, mapa_add[sel_add]):
                        st.success("Aluno adicionado!")
                    else:
                        st.warning("Este aluno ja pertence a um time.")
                    st.rerun()
            else:
                st.info("Nenhum aluno disponivel.")

    with col2:
        with st.container(border=True):
            st.markdown("**Remover membro**")
            mapa_rm = {
                m.get("nome"): m.get("id")
                for m in membros
                if isinstance(m, dict) and m.get("nome") and m.get("id")
            }
            if mapa_rm:
                sel_rm = st.selectbox("Membro", list(mapa_rm.keys()), key="rm_aluno")
                if st.button("Remover", use_container_width=True):
                    remover_aluno(time_id, mapa_rm[sel_rm])
                    st.success("Membro removido.")
                    st.rerun()
            else:
                st.info("Nenhum membro para remover.")

    st.divider()

    with st.expander("Mover aluno para outro time", expanded=False):
        todos_times = listar_times()
        mapa_times  = {
            t.get("nome"): t.get("id")
            for t in todos_times
            if isinstance(t, dict) and t.get("nome") and t.get("id")
        }
        mapa_mv = {
            m.get("nome"): m.get("id")
            for m in membros
            if isinstance(m, dict) and m.get("nome") and m.get("id")
        }
        if mapa_mv and mapa_times:
            col3, col4 = st.columns(2)
            with col3:
                aluno_mv = st.selectbox("Aluno", list(mapa_mv.keys()), key="mover_aluno")
            with col4:
                destino  = st.selectbox("Destino", list(mapa_times.keys()), key="mover_destino")
            if st.button("Mover", use_container_width=True):
                mover_aluno(mapa_mv[aluno_mv], mapa_times[destino])
                st.success("Aluno movido!")
                st.rerun()
        else:
            st.info("Sem dados suficientes para mover alunos.")
import streamlit as st
from database.conexao import supabase
from services.batalha_de_equipes_service import (
    listar_times, listar_membros_time, listar_alunos,
    adicionar_aluno, remover_aluno, mover_aluno
)
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
        st.error("Sessao invalida.")
        return

    if tipo == "professor":
        times = listar_times()
        if not times:
            st.warning("Nenhum time cadastrado.")
            return
        mapa = {
            t.get("nome"): t.get("id")
            for t in times
            if isinstance(t, dict) and t.get("nome") and t.get("id")
        }
        if not mapa:
            st.warning("Times com dados invalidos.")
            return
        sel     = st.selectbox("Selecione o time", list(mapa.keys()))
        time_id = mapa[sel]

    else:
        res  = supabase.table("time_membros") \
            .select("time_id, times(id,nome)") \
            .eq("usuario_id", user_id) \
            .execute()
        data = _safe_list(getattr(res, "data", None))

        if not data:
            st.markdown("""
            <div style="
                background:#fff3e0;
                border-left:4px solid #0d1b2a;
                border-radius:8px;
                padding:14px 18px;
            ">
                <strong style="color:#0d1b2a;">Voce nao participa de nenhum time ainda.</strong>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Entrar em um time"):
                st.session_state.pagina = "batalha_times"
                st.rerun()
            return

        first_row = _safe_dict(data[0])
        time_info = first_row.get("times")
        if isinstance(time_info, list):
            time_info = time_info[0] if time_info else {}
        time_info = _safe_dict(time_info)

        if not time_info.get("id") or not time_info.get("nome"):
            st.error("Erro ao carregar time.")
            return

        time_id = time_info["id"]
        st.markdown(f"""
        <div style="
            background:#e0f7fa;
            border-left:4px solid #00b4d8;
            border-radius:8px;
            padding:12px 16px;
            margin-bottom:12px;
        ">
            <strong style="color:#0d1b2a;">Seu time: {time_info['nome']}</strong>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Membros")

    membros = listar_membros_time(time_id)

    if not membros:
        st.info("Nenhum membro neste time.")
    else:
        st.dataframe(
            membros,
            column_config={
                "id":    st.column_config.NumberColumn("ID"),
                "nome":  st.column_config.TextColumn("Nome"),
                "email": st.column_config.TextColumn("E-mail"),
            },
            use_container_width=True,
            hide_index=True
        )

    if tipo != "professor":
        return

    st.divider()
    st.markdown("### Gestao de membros")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("**Adicionar aluno**")
            alunos   = listar_alunos()
            mapa_add = {
                a.get("nome"): a.get("id")
                for a in alunos
                if isinstance(a, dict) and a.get("nome") and a.get("id")
            }
            if mapa_add:
                sel_add = st.selectbox("Aluno", list(mapa_add.keys()), key="add_aluno")
                if st.button("Adicionar", use_container_width=True):
                    if adicionar_aluno(time_id, mapa_add[sel_add]):
                        st.success("Aluno adicionado!")
                    else:
                        st.warning("Este aluno ja pertence a um time.")
                    st.rerun()
            else:
                st.info("Nenhum aluno disponivel.")

    with col2:
        with st.container(border=True):
            st.markdown("**Remover membro**")
            mapa_rm = {
                m.get("nome"): m.get("id")
                for m in membros
                if isinstance(m, dict) and m.get("nome") and m.get("id")
            }
            if mapa_rm:
                sel_rm = st.selectbox("Membro", list(mapa_rm.keys()), key="rm_aluno")
                if st.button("Remover", use_container_width=True):
                    remover_aluno(time_id, mapa_rm[sel_rm])
                    st.success("Membro removido.")
                    st.rerun()
            else:
                st.info("Nenhum membro para remover.")

    st.divider()

    with st.expander("Mover aluno para outro time", expanded=False):
        todos_times = listar_times()
        mapa_times  = {
            t.get("nome"): t.get("id")
            for t in todos_times
            if isinstance(t, dict) and t.get("nome") and t.get("id")
        }
        mapa_mv = {
            m.get("nome"): m.get("id")
            for m in membros
            if isinstance(m, dict) and m.get("nome") and m.get("id")
        }
        if mapa_mv and mapa_times:
            col3, col4 = st.columns(2)
            with col3:
                aluno_mv = st.selectbox("Aluno", list(mapa_mv.keys()), key="mover_aluno")
            with col4:
                destino  = st.selectbox("Destino", list(mapa_times.keys()), key="mover_destino")
            if st.button("Mover", use_container_width=True):
                mover_aluno(mapa_mv[aluno_mv], mapa_times[destino])
                st.success("Aluno movido!")
                st.rerun()
        else:
            st.info("Sem dados suficientes para mover alunos.")
