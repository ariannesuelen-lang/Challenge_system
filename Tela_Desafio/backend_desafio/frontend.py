import streamlit as st
import pandas as pd
from datetime import date
from backend_desafio import criar_desafio, listar_desafios, deletar_desafio, atualizar_desafio

st.set_page_config(page_title="Painel de Desafios", layout="centered")
st.title("🎯 Gestão de Desafios")

aba_criar, aba_listar, aba_editar, aba_deletar = st.tabs([ "Criar Novo", "Listar", "Editar", "Deletar"])

# --- ABA LISTAR ---
with aba_listar:
    st.header("📋 Desafios Cadastrados")
    try:
        desafios = listar_desafios()
        if not desafios:
            st.info("Nenhum desafio encontrado no banco.")
        else:
            df = pd.DataFrame(desafios)
            if "data_criacao" in df.columns:
                df["data_criacao"] = pd.to_datetime(df["data_criacao"]).dt.strftime('%d/%m/%Y')
            if "data_limite" in df.columns:
                df["data_limite"] = pd.to_datetime(df["data_limite"]).dt.strftime('%d/%m/%Y')
            st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Erro ao conectar com o banco: {e}")

# --- ABA CRIAR ---
with aba_criar:
    st.header("➕ Adicionar Desafio")
    with st.form("form_criar"):
        titulo = st.text_input("Título do Desafio")
        descricao = st.text_area("Descrição")
        col1, col2 = st.columns(2)
        criador_id = col1.number_input("ID do Criador", min_value=1, step=1)
        disciplina_id = col2.number_input("ID da Disciplina", min_value=1, step=1)
        data_limite = st.date_input("Data Limite")
        
        
        if st.form_submit_button("Salvar Desafio"):
            # Chama o backend e guarda a resposta padronizada
            resposta_backend = criar_desafio(titulo, descricao, criador_id, disciplina_id, data_limite)
            
            # Lê o dicionário para saber se deu certo ou errado
            if resposta_backend["sucesso"] == True:
                st.success("Desafio salvo com sucesso no banco!")
                st.rerun()
            else:
                # Se o backend barrou, mostra a mensagem de erro que o backend enviou!
                st.warning(resposta_backend["mensagem"])
# --- ABA EDITAR ---
with aba_editar:
    st.header("✏️ Editar Desafio")
    desafios = listar_desafios()
    if desafios:
        opcoes = {d["id"]: f"{d['id']} - {d['titulo']}" for d in desafios}
        id_escolhido = st.selectbox("Escolha o desafio:", options=list(opcoes.keys()), format_func=lambda x: opcoes[x])
        desafio_atual = next((d for d in desafios if d["id"] == id_escolhido), None)
        
        with st.form("form_editar"):
            novo_titulo = st.text_input("Título", value=desafio_atual.get("titulo", ""))
            nova_descricao = st.text_area("Descrição", value=desafio_atual.get("descricao", ""))
            if st.form_submit_button("Atualizar"):
                atualizar_desafio(id_escolhido, {"titulo": novo_titulo, "descricao": nova_descricao})
                st.success("Atualizado!")
                st.rerun()

# --- ABA DELETAR ---
with aba_deletar:
    st.header("🗑️ Deletar Desafio")
    desafios = listar_desafios()
    if desafios:
        opcoes = {d["id"]: f"{d['id']} - {d['titulo']}" for d in desafios}
        id_deletar = st.selectbox("Escolha para APAGAR:", options=list(opcoes.keys()), format_func=lambda x: opcoes[x])
        if st.button("Confirmar Exclusão", type="primary"):
            deletar_desafio(id_deletar)
            st.success("Deletado!")
            st.rerun()