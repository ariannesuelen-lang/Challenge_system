import streamlit as st
from datetime import date
from services.batalha_de_equipes_service import (
    listar_batalhas, criar_batalha, finalizar_batalha
)


def tela_batalha_gerenciar():

    usuario = st.session_state.usuario_logado
    tipo    = usuario.get("tipo_usuario", "aluno")
    user_id = usuario.get("id")

    if tipo not in ("professor", "admin"):
        st.error("Acesso restrito a professores.")
        return

    st.title("Gerenciar Batalhas")

    if st.button("Voltar"):
        st.session_state.pagina = "batalha_de_equipes"
        st.rerun()

    st.divider()

    st.subheader("Nova Batalha")

    with st.container(border=True):

        titulo    = st.text_input("Titulo da batalha")
        descricao = st.text_area("Descricao / objetivo")

        col1, col2 = st.columns(2)
        with col1:
            quantidade_rodadas = st.number_input("Numero de rodadas", min_value=1, step=1, value=3)
        with col2:
            tempo_por_rodada = st.number_input("Tempo por rodada (min)", min_value=1, step=1, value=30)

        prazo = st.date_input("Prazo", value=None, min_value=date.today())

        regras = st.text_area(
            "Regras de conduta",
            value="Siga as regras de Fair Play da instituicao."
        )

        st.markdown("**Criterios de avaliacao** (um por linha)")
        criterios_raw = st.text_area(
            "Criterios",
            placeholder="Logica\nOrganizacao\nCriatividade"
        )
        criterios = [c.strip() for c in criterios_raw.splitlines() if c.strip()]

        st.markdown("**Configuracoes de seguranca**")
        col3, col4, col5 = st.columns(3)
        with col3:
            bloquear_copia   = st.checkbox("Bloquear copia", value=True)
        with col4:
            verificar_plagio = st.checkbox("Verificar plagio", value=True)
        with col5:
            limitar_ip       = st.checkbox("Limitar IP", value=False)

        seguranca = {
            "bloquear_copia":   bloquear_copia,
            "verificar_plagio": verificar_plagio,
            "limitar_IP":       limitar_ip
        }

        if st.button("Criar batalha"):
            if not titulo.strip():
                st.warning("O titulo e obrigatorio.")
            else:
                batalhas_existentes = listar_batalhas()
                titulos_existentes = [
                    b.get("titulo", "").strip().lower()
                    for b in batalhas_existentes
                    if isinstance(b, dict)
                ]
                if titulo.strip().lower() in titulos_existentes:
                    st.error(f"Ja existe uma batalha com o titulo '{titulo.strip()}'.")
                elif criar_batalha(
                    titulo, descricao, user_id,
                    quantidade_rodadas, tempo_por_rodada,
                    criterios, regras, seguranca, prazo
                ):
                    st.success("Batalha criada com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao criar batalha.")

    st.divider()
    st.subheader("Batalhas cadastradas")

    batalhas = listar_batalhas()

    if not batalhas:
        st.info("Nenhuma batalha cadastrada ainda.")
        return

    for b in batalhas:

        bid        = b.get("id")
        finalizada = b.get("finalizada", False)
        status_txt = "Finalizada" if finalizada else "Em aberto"

        with st.container(border=True):

            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**{b.get('titulo')}**")
                st.caption(
                    f"Status: {status_txt} | "
                    f"Rodadas: {b.get('quantidade_rodadas', '-')} | "
                    f"Prazo: {b.get('prazo') or 'sem prazo'}"
                )
                if b.get("descricao"):
                    st.write(b["descricao"])

                criterios_lista = b.get("criterios_avaliacao") or []
                if criterios_lista:
                    with st.expander("Criterios"):
                        for c in criterios_lista:
                            st.markdown(f"- {c}")

                if b.get("regras_conduta"):
                    with st.expander("Regras"):
                        st.write(b["regras_conduta"])

            with col2:
                if not finalizada:
                    if st.button("Finalizar", key=f"fin_{bid}"):
                        finalizar_batalha(bid)
                        st.success("Batalha finalizada.")
                        st.rerun()
                else:
                    st.info("Encerrada")
