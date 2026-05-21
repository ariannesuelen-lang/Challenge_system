import streamlit as st
from conexao import buscar_voto_por_id, atualizar_voto, deletar_voto
from modules.utils import ir

MAPA_VOTO = {
    "👍\n\nBom": "Bom",
    "😐\n\nRegular": "Regular",
    "👎\n\nRuim": "Ruim"
}

def _normalizar(voto):
    return MAPA_VOTO.get(voto, voto).strip().capitalize()

def render():
    if st.button("← Voltar", key="btn_voltar_editar"):
        ir('visualizar')

    id_voto = st.session_state.voto_id
    dados = buscar_voto_por_id(id_voto)

    if not dados.data:
        st.error("Voto não encontrado")
        return

    voto_atual = _normalizar(dados.data[0]["voto"])
    desafio = dados.data[0]["desafio"]
    st.write(f"### {desafio} | Editar voto ID {id_voto}")

    opcoes = ["Bom", "Regular", "Ruim"]
    novo_voto = st.radio(
        "Novo voto:",
        opcoes,
        index=opcoes.index(voto_atual) if voto_atual in opcoes else 0
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Atualizar"):
            atualizar_voto(id_voto, novo_voto)
            st.success("Voto atualizado")
    with col2:
        if st.button("Excluir"):
            deletar_voto(id_voto)
            st.success("Voto excluído")