import streamlit as st
from supabase import create_client
import pandas as pd

# =========================
# CONEXÃO COM SUPABASE
# =========================

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]

supabase = create_client(url, key)

st.set_page_config(page_title="Votação de Desafios", layout="centered")

# =========================
# CONTROLE DE ESTADO
# =========================

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'lista'

if 'voto_id' not in st.session_state:
    st.session_state.voto_id = None

if 'desafio' not in st.session_state:
    st.session_state.desafio = None

def ir(pagina):
    st.session_state.pagina = pagina
    st.rerun()

# =========================
# FUNÇÕES CRUD
# =========================

def inserir_voto(usuario, desafio, voto):
    return supabase.table("votos").insert({
        "usuario": usuario,
        "desafio": desafio,
        "voto": voto
    }).execute()

def listar_votos():
    return supabase.table("votos").select("*").execute()

def buscar_voto_por_id(id):
    return supabase.table("votos").select("*").eq("id", id).execute()

def atualizar_voto(id, novo_voto):
    return supabase.table("votos").update({
        "voto": novo_voto
    }).eq("id", id).execute()

def deletar_voto(id):
    return supabase.table("votos").delete().eq("id", id).execute()

# =========================
# HEADER
# =========================

col1, col2 = st.columns([4, 1])
with col2:
    st.markdown("👤 *Aluno*")

st.divider()

# =========================
# LISTA DE DESAFIOS
# =========================

if st.session_state.pagina == 'lista':

    st.write("### Lista de Desafios")

    # Simulação de múltiplos desafios
    desafios = [
        "Desafio 01 - A Realidade vs. A Teoria",
        "Desafio 02 - Testes Experimentais"
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

# =========================
# VOTAÇÃO (CREATE)
# =========================

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

            # volta automaticamente para lista
            st.session_state.desafio = None
            ir('lista')

        except Exception as e:
            st.error(e)

# =========================
# VISUALIZAR VOTOS (READ)
# =========================

elif st.session_state.pagina == 'visualizar':

    if st.button("← Voltar"):
        ir('lista')

    st.write("### Votos cadastrados")

    dados = listar_votos()

    if dados.data:
        df = pd.DataFrame(dados.data)
        st.write(df)

        st.divider()

        id_voto = st.number_input("Digite o ID do voto", step=1)

        if st.button("Editar / Excluir"):
            st.session_state.voto_id = id_voto
            ir('editar')

    else:
        st.info("Nenhum voto encontrado")

# =========================
# EDITAR / EXCLUIR (UPDATE / DELETE)
# =========================

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
