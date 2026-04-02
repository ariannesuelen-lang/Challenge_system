import streamlit as st
import sqlite3

# --- Configuração do banco de dados ---
conn = sqlite3.connect("academico.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS desafio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    nivel TEXT NOT NULL
)
""")
conn.commit()

# --- Funções CRUD ---
def inserir_desafio(titulo, descricao, nivel):
    c.execute("INSERT INTO desafio (titulo, descricao, nivel) VALUES (?, ?, ?)", (titulo, descricao, nivel))
    conn.commit()

def listar_desafios():
    c.execute("SELECT * FROM desafio")
    return c.fetchall()

def atualizar_desafio(id, titulo, descricao, nivel):
    c.execute("UPDATE desafio SET titulo=?, descricao=?, nivel=? WHERE id=?", (titulo, descricao, nivel, id))
    conn.commit()

def deletar_desafio(id):
    c.execute("DELETE FROM desafio WHERE id=?", (id,))
    conn.commit()

# --- Interface Streamlit ---
st.title(" Sistema Acadêmico - CRUD de Desafios")

menu = st.sidebar.selectbox("Menu", ["Criar", "Listar", "Atualizar", "Deletar"])

if menu == "Criar":
    st.subheader("Adicionar novo desafio")
    titulo = st.text_input("Título")
    descricao = st.text_area("Descrição")
    nivel = st.selectbox("Nível", ["Fácil", "Médio", "Difícil"])
    if st.button("Salvar"):
        inserir_desafio(titulo, descricao, nivel)
        st.success("Desafio adicionado com sucesso!")

elif menu == "Listar":
    st.subheader("Lista de desafios")
    desafios = listar_desafios()
    for d in desafios:
        st.write(f"ID: {d[0]} | Título: {d[1]} | Nível: {d[3]}")
        st.write(f"Descrição: {d[2]}")
        st.write("---")

elif menu == "Atualizar":
    st.subheader("Atualizar desafio")
    desafios = listar_desafios()
    ids = [d[0] for d in desafios]
    id_escolhido = st.selectbox("Selecione o ID", ids)
    titulo = st.text_input("Novo título")
    descricao = st.text_area("Nova descrição")
    nivel = st.selectbox("Novo nível", ["Fácil", "Médio", "Difícil"])
    if st.button("Atualizar"):
        atualizar_desafio(id_escolhido, titulo, descricao, nivel)
        st.success("Desafio atualizado com sucesso!")

elif menu == "Deletar":
    st.subheader("Deletar desafio")
    desafios = listar_desafios()
    ids = [d[0] for d in desafios]
    id_escolhido = st.selectbox("Selecione o ID para deletar", ids)
    if st.button("Deletar"):
        deletar_desafio(id_escolhido)
        st.warning("Desafio deletado com sucesso!")