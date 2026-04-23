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
@st.cache_data(ttl=30)
def listar_votos():
    return supabase.table("votos").select("*").execute()
    
@st.cache_data(ttl=30)
def buscar_votos_por_desafio(desafio):
    return supabase.table("votos").select("*").eq("desafio", desafio).execute()

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
# VOTAÇÃO + GRÁFICO
# =========================

elif st.session_state.pagina == 'votacao':

    if st.button("← Voltar"):
        ir('lista')

    desafio = st.session_state.desafio

    st.write(f"### {desafio} | Votação")

    voto = st.radio("Escolha sua nota:", ["Bom", "Regular", "Ruim"])

    # controle de envio
if 'enviando' not in st.session_state:
    st.session_state.enviando = False

if st.button("Enviar Voto", disabled=st.session_state.enviando):

    if voto is None:
        st.warning("Selecione uma opção antes de enviar.")
        st.stop()

    st.session_state.enviando = True

    try:
        with st.spinner("Salvando voto..."):
            inserir_voto("AlunoTeste", desafio, voto)

        st.success("Voto salvo com sucesso")

        st.session_state.enviando = False
        st.session_state.desafio = None
        ir('lista')

    except Exception as e:
        st.session_state.enviando = False
        st.error("Erro ao salvar voto.")
        st.exception(e)

    # =========================
    # GRÁFICO DE VOTOS
    # =========================

    st.divider()
    st.write("### Resultado do Desafio")

    dados = buscar_votos_por_desafio(desafio)

    if dados.data:
        df = pd.DataFrame(dados.data)

        # conta quantos votos existem de cada tipo
        contagem = df["voto"].value_counts()

        # garante que todas opções apareçam
        contagem = contagem.reindex(["Bom", "Regular", "Ruim"], fill_value=0)

        st.bar_chart(contagem, use_container_width=True)
        
    else:
        st.info("Nenhum voto ainda")

# =========================
# VISUALIZAR VOTOS
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
        if id_voto is None or id_voto <= 0:
           st.warning("Digite um ID válido.")
           st.stop()

        if st.button("Editar / Excluir"):
            st.session_state.voto_id = id_voto
            ir('editar')

    else:
        st.info("Nenhum voto encontrado")

# =========================
# EDITAR / EXCLUIR
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
