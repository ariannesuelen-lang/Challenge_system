import streamlit as st
from supabase import create_client, Client
from datetime import date, datetime

# --- 1. CONEXÃO COM O BANCO ---
@st.cache_resource
def iniciar_conexao():
    url = st.secrets["SUPABASE_URL"]
    chave = st.secrets["SUPABASE_KEY"]
    return create_client(url, chave)

banco = iniciar_conexao()

# --- 2. MENU LATERAL ---
# Cria a barra lateral e guarda a escolha do usuário na variável 'menu'
menu = st.sidebar.selectbox("Menu", ["Criar", "Listar", "Atualizar", "Deletar"])

st.title("Sistema Acadêmico - CRUD de Desafios")

# --- 3. TELA DE CRIAR DESAFIO ---
if menu == "Criar":
    st.header("Adicionar novo desafio")
    
    # Criando os campos do formulário
    titulo = st.text_input("Título")
    descricao = st.text_area("Descrição")
    nivel = st.selectbox("Nível", ["Fácil", "Médio", "Difícil"])
    prazo = st.date_input("Prazo do Desafio")
    data_postagem = st.date_input("Data de Postagem", value=date.today()) # Já vem com a data de hoje preenchida
    
    # Botão de salvar
    if st.button("Salvar"):
        # Se o usuário não digitar o título, pedimos para preencher
        if not titulo:
            st.warning("O campo Título é obrigatório!")
        else:
            # Montamos o "pacote" de dados com os mesmos nomes das colunas do banco
            novo_desafio = {
                "titulo": titulo,
                "descricao": descricao,
                "nivel": nivel,
                "prazo": str(prazo), # O banco pede texto, então convertemos a data para string
                "data_postagem": str(data_postagem)
            }
            
            try:
                # Enviamos o pacote para a tabela 'tela_desafio'
                banco.table("tela_desafio").insert(novo_desafio).execute()
                st.success("Desafio adicionado com sucesso!")
            except Exception as e:
                st.error(f"Ocorreu um erro ao salvar no banco: {e}")
 # --- 4. TELA DE LISTAR DESAFIOS ---
elif menu == "Listar":
    st.header("Lista de desafios")
    
    try:
        # Pede para o Supabase trazer todos os registros da tabela
        resposta = banco.table("tela_desafio").select("*").execute()
        desafios = resposta.data # Aqui fica a lista com os dados
        
        # Verifica se o banco está vazio
        if not desafios:
            st.info("Nenhum desafio cadastrado ainda. Vá na aba 'Criar' para adicionar um!")
        else:
            # Se tiver dados, fazemos um loop (for) para desenhar cada um na tela
            for d in desafios:
                # Usamos st.container() para deixar cada desafio num "bloquinho" visual
                with st.container(border=True):
                    st.subheader(f"{d['id']} - {d['titulo']}")
                    st.markdown(f"**Nível:** {d['nivel']}")
                    st.write(f"**Descrição:** {d['descricao']}")
                    
                    # Colocamos as datas menores no canto inferior
                    st.caption(f"Postado em: {d['data_postagem']} | Prazo: {d['prazo']}")
            
    except Exception as e:
        st.error(f"Erro ao buscar os dados: {e}")               
# --- 5. TELA DE DELETAR DESAFIOS ---
elif menu == "Deletar":
    st.header("Deletar desafio")
    
    try:
        # Busca apenas ID e Título no banco para montar a lista
        resposta = banco.table("tela_desafio").select("id, titulo").execute()
        desafios = resposta.data
        
        if not desafios:
            st.info("Não há desafios para deletar.")
        else:
            # Cria um dicionário para facilitar a exibição no selectbox
            opcoes = {d["id"]: f"ID {d['id']} - {d['titulo']}" for d in desafios}
            
            # O selectbox mostra o texto, mas guarda apenas o ID do desafio escolhido
            id_selecionado = st.selectbox("Selecione o desafio", options=list(opcoes.keys()), format_func=lambda x: opcoes[x])
            
            if st.button("Deletar Desafio"): 
                # O comando mágico que deleta a linha específica no Supabase
                banco.table("tela_desafio").delete().eq("id", id_selecionado).execute()
                
                st.success("Desafio deletado com sucesso!")
                st.rerun() # Atualiza a tela automaticamente para a lista nova
                
    except Exception as e:
        st.error(f"Erro ao tentar deletar: {e}")
# --- 6. TELA DE ATUALIZAR DESAFIOS ---
elif menu == "Atualizar":
    st.header("Atualizar desafio")
    
    try:
        # Busca todos os dados para poder preencher o formulário depois
        resposta = banco.table("tela_desafio").select("*").execute()
        desafios = resposta.data
        
        if not desafios:
            st.info("Não há desafios para atualizar.")
        else:
            opcoes = {d["id"]: f"ID {d['id']} - {d['titulo']}" for d in desafios}
            id_selecionado = st.selectbox("Selecione o desafio para editar", options=list(opcoes.keys()), format_func=lambda x: opcoes[x])
            
            # Filtra na nossa lista qual foi o desafio exato que o usuário escolheu
            desafio_atual = next(d for d in desafios if d["id"] == id_selecionado)
            
            # --- Formulário preenchido com os dados antigos ---
            # O parâmetro 'value' é o que preenche os campos com os dados do banco
            titulo_novo = st.text_input("Título", value=desafio_atual["titulo"])
            descricao_nova = st.text_area("Descrição", value=desafio_atual["descricao"])
            
            niveis = ["Fácil", "Médio", "Difícil"]
            idx_nivel = niveis.index(desafio_atual["nivel"]) if desafio_atual["nivel"] in niveis else 0
            nivel_novo = st.selectbox("Nível", niveis, index=idx_nivel)
            
            # Converte a data do banco (que é texto) de volta para o formato de data do Python
            prazo_antigo = datetime.strptime(desafio_atual["prazo"], "%Y-%m-%d").date() if desafio_atual["prazo"] else date.today()
            data_postagem_antiga = datetime.strptime(desafio_atual["data_postagem"], "%Y-%m-%d").date() if desafio_atual["data_postagem"] else date.today()
            
            prazo_novo = st.date_input("Prazo do Desafio", value=prazo_antigo)
            data_postagem_nova = st.date_input("Data de Postagem", value=data_postagem_antiga)
            
            # --- Botão de Salvar Alterações ---
            if st.button("Salvar Alterações"):
                dados_atualizados = {
                    "titulo": titulo_novo,
                    "descricao": descricao_nova,
                    "nivel": nivel_novo,
                    "prazo": str(prazo_novo),
                    "data_postagem": str(data_postagem_nova)
                }
                
                # O update precisa do .eq() para saber qual ID ele vai alterar
                banco.table("tela_desafio").update(dados_atualizados).eq("id", id_selecionado).execute()
                
                st.success("Desafio atualizado com sucesso!")
                
    except Exception as e:
        st.error(f"Erro ao tentar atualizar: {e}")
        