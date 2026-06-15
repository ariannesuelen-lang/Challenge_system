import streamlit as st
import pandas as pd

from services.votacao_service import (
    buscar_voto_usuario,
    registrar_voto,
    atualizar_voto,
    deletar_voto,
    listar_votos_desafio
)
from utils.estilo import aplicar_estilo, cabecalho


def tela_voto():

    aplicar_estilo()

    if "desafio_voto" not in st.session_state or not st.session_state.desafio_voto:
        st.warning("Nenhum desafio selecionado.")
        if st.button("Voltar"):
            st.session_state.pagina = "votacao"
            st.rerun()
        return

    desafio = st.session_state.desafio_voto
    usuario = st.session_state.usuario_logado

    cabecalho(desafio["titulo"], f"Prazo: {desafio.get('data_limite', '-')}")

    if st.button("Voltar para votacao"):
        st.session_state.pagina = "votacao"
        st.rerun()

    st.divider()

    opcoes = ["Bom", "Regular", "Ruim"]

    voto_existente = buscar_voto_usuario(
        usuario["email"],
        desafio["titulo"]
    )

    editar = False

    if voto_existente:

        st.markdown(f"""
        <div style="
            background:#e0f7fa;
            border-left:4px solid #00b4d8;
            border-radius:8px;
            padding:12px 16px;
            margin-bottom:12px;
        ">
            <strong style="color:#0d1b2a;">Seu voto atual:</strong>
            <span style="color:#00b4d8; font-weight:700; margin-left:8px;">
                {voto_existente['voto']}
            </span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Editar voto"):
            st.session_state.editando_voto = True
            st.rerun()

        editar = st.session_state.get("editando_voto", False)

    else:
        editar = True

    if editar:

        st.markdown("### Escolha seu voto")

        voto = st.radio(
            "Opcoes de voto",
            opcoes,
            key="radio_voto_opcoes",
            label_visibility="collapsed"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if voto_existente:

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Salvar edicao", use_container_width=True):
                    atualizar_voto(voto_existente["id"], voto)
                    st.session_state.editando_voto = False
                    st.success("Voto atualizado!")
                    st.rerun()

            with col2:
                if st.button("Excluir voto", use_container_width=True):
                    deletar_voto(voto_existente["id"])
                    st.session_state.editando_voto = False
                    st.success("Voto excluido!")
                    st.rerun()

        else:

            if st.button("Enviar voto", use_container_width=True):
                registrar_voto(usuario["email"], desafio["titulo"], voto)
                st.success("Voto registrado!")
                st.rerun()

    st.divider()

    if "mostrar_resultado" not in st.session_state:
        st.session_state.mostrar_resultado = False

    if st.button("Mostrar / Ocultar resultados"):
        st.session_state.mostrar_resultado = not st.session_state.mostrar_resultado
        st.rerun()

    if st.session_state.mostrar_resultado:

        votos = listar_votos_desafio(desafio["titulo"])

        if not votos:
            st.warning("Nenhum voto encontrado.")
            return

        df       = pd.DataFrame(votos)
        contagem = df["voto"].value_counts().reindex(opcoes, fill_value=0)

        st.markdown("### Resultado")

        col1, col2, col3 = st.columns(3)
        cores = {"Bom": "#00b4d8", "Regular": "#1b3a5c", "Ruim": "#e94560"}

        for col, opcao in zip([col1, col2, col3], opcoes):
            with col:
                st.markdown(f"""
                <div style="
                    background:#f0f9ff;
                    border-left:4px solid {cores[opcao]};
                    border-radius:8px;
                    padding:12px;
                    text-align:center;
                ">
                    <p style="color:#555; margin:0; font-size:13px;">{opcao}</p>
                    <h2 style="color:{cores[opcao]}; margin:4px 0;">{contagem[opcao]}</h2>
                    <p style="color:#aaa; margin:0; font-size:11px;">votos</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.bar_chart(contagem)
        st.caption(f"Total de votos: {len(df)}")

        if usuario["tipo_usuario"] in ("professor", "admin"):

            st.divider()
            st.markdown("### Gerenciar votos")

            filtro = st.selectbox(
                "Filtrar por voto",
                ["Todos"] + opcoes,
                key="filtro_votos_admin"
            )

            votos_filtrados = votos if filtro == "Todos" else [
                v for v in votos if v["voto"] == filtro
            ]

            if not votos_filtrados:
                st.info("Nenhum voto encontrado.")
                return

            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            col1.markdown("**Usuario**")
            col2.markdown("**Voto**")
            col3.markdown("**Salvar**")
            col4.markdown("**Excluir**")
            st.divider()

            for v in votos_filtrados:

                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

                with col1:
                    st.write(v["usuario"])

                with col2:
                    novo_voto = st.selectbox(
                        "Voto",
                        opcoes,
                        index=opcoes.index(v["voto"]) if v["voto"] in opcoes else 0,
                        key=f"select_voto_{v['id']}",
                        label_visibility="collapsed"
                    )

                with col3:
                    if st.button("Salvar", key=f"salvar_voto_{v['id']}"):
                        atualizar_voto(v["id"], novo_voto)
                        st.success("Atualizado!")
                        st.rerun()

                with col4:
                    if st.button("Excluir", key=f"excluir_voto_{v['id']}"):
                        deletar_voto(v["id"])
                        st.success("Excluido!")
                        st.rerun()
