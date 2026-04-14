import streamlit as st

# CONEXAO COM BACKEND
from conexao import (
    inserir_voto,
    listar_votos,
    buscar_voto_por_id,
    atualizar_voto,
    deletar_voto
)
import pandas as pd

st.set_page_config(page_title="Votação de Desafios", layout="centered")

# CONTROLE DE ESTADO
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'lista'

if 'voto_id' not in st.session_state:
    st.session_state.voto_id = None

if 'desafio' not in st.session_state:
    st.session_state.desafio = None

# NAVEGAÇÃO
def ir(pagina):
    st.session_state.pagina = pagina
    st.rerun()


# HEADER
col1, col2 = st.columns([4, 1])
with col2:
    st.markdown("👤 *Aluno*")

st.divider()

# LISTA DE DESAFIOS
if st.session_state.pagina == 'lista':

    st.write("### Lista de Desafios")

    desafios = [
        "Desafio 01 - Como conectar com Supabase",
        "Desafio 02 - Teste"
    ]

    for d in desafios:
        with st.container(border=True):
            st.write(f"### {d}")
            st.caption("em andamento")

            if st.button(f"Acessar {d}"):
                st.session_state.desafio = d
                ir('votacao')

    st.divider()

    if st.button("Ver votos cadastrados"):
        ir('visualizar')

# VOTAÇÃO 
elif st.session_state.pagina == 'votacao':

    if st.button("← Voltar"):
        ir('lista')

    desafio = st.session_state.desafio

    st.write(f"### {desafio} | Votação")

    voto = st.radio("Escolha sua nota:", ["Bom", "Regular", "Ruim"])

    if st.button("Enviar Voto"):
        try:
            inserir_voto("AlunoTeste", desafio, voto)
            st.success("Voto salvo com sucesso")

            st.session_state.desafio = None
            ir('lista')

        except Exception as e:
            st.error(e)

 

# VISUALIZAR VOTOS
elif st.session_state.pagina == 'visualizar':

    if st.button("← Voltar"):
        ir('lista')

    st.write("### Votos cadastrados")

    dados = listar_votos()

    if dados.data:
        df = pd.DataFrame(dados.data)

        # TABELA
        st.write(df)

        st.divider()

        # GRÁFICO GERAL
        st.write("### Resultado Geral")

        contagem = df["voto"].value_counts()
        contagem = contagem.reindex(["Bom", "Regular", "Ruim"], fill_value=0)

        st.bar_chart(contagem)

        st.divider()

   
        # GRÁFICO POR DESAFIO
        desafios_unicos = df["desafio"].unique()

        desafio_selecionado = st.selectbox(
            "Filtrar por desafio",
            desafios_unicos
        )

        df_filtrado = df[df["desafio"] == desafio_selecionado]

        st.write(f"### Resultado - {desafio_selecionado}")

        contagem_filtrada = df_filtrado["voto"].value_counts()
        contagem_filtrada = contagem_filtrada.reindex(["Bom", "Regular", "Ruim"], fill_value=0)

        st.bar_chart(contagem_filtrada)

        st.divider()


        # EDITAR / EXCLUIR
        id_voto = st.number_input("Digite o ID do voto", step=1)

        if st.button("Editar / Excluir"):
            st.session_state.voto_id = id_voto
            ir('editar')

    else:
        st.info("Nenhum voto encontrado")



# EDITAR E EXCLUIR VOTO
elif st.session_state.pagina == 'editar':

    if st.button("← Voltar"):
        ir('visualizar')

    id_voto = st.session_state.voto_id

    dados = buscar_voto_por_id(id_voto)

    if dados.data:

        voto_atual = dados.data[0]["voto"]
        desafio = dados.data[0]["desafio"]

        st.write(f"### {desafio} | Editar voto ID {id_voto}")

        novo_voto = st.radio(
            "Novo voto:",
            ["Bom", "Regular", "Ruim"],
            index=["Bom", "Regular", "Ruim"].index(voto_atual)
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

    else:
        st.error("Voto não encontrado")
