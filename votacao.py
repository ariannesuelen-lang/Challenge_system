import streamlit as st    # Importa a biblioteca Streamlit
import pandas as pd       # Importa a biblioteca pandas para manipular os dados em formato de tabela

# CONEXAO COM BACKEND
from conexao import (    # Importa funções do arquivo conexao.py (ele que vai mexer no banco de dados)
    inserir_voto,        # função para salvar um voto
    listar_votos,        # função para buscar todos os votos
    buscar_voto_por_id,  # função para buscar um voto específico pelo ID
    atualizar_voto,      # função para atualizar um voto
    deletar_voto         # função para excluir um voto
)

st.set_page_config(page_title="Votação de Desafios", layout="centered")        # Configura o título da aba do navegador e o layout da página


# CONTROLE DE ESTADO (essa parte é para salvar temporariamente as escolhas do usuário antes de cada mudança de tela. Sim, é importante ;-; favor não mexer)
if 'pagina' not in st.session_state:     # Verifica se a variável 'pagina' já existe na sessão e se não existir, cria e define como 'lista'
    st.session_state.pagina = 'lista'
 
if 'voto_id' not in st.session_state:    # Armazena o ID do voto que será editado/excluído
    st.session_state.voto_id = None

if 'desafio' not in st.session_state:    # Armazena qual desafio foi selecionado
    st.session_state.desafio = None

# Simulando o ID do usuário logado
if 'id_usuario' not in st.session_state: # Armazena o ID dinâmico do usuário (para evitar votos duplicados)
    st.session_state.id_usuario = "user_123" # ID gerado pelo time de login


# FUNÇÃO DE NAVEGAÇÃO
def ir(pagina):                           # Função para mudar de página
    st.session_state.pagina = pagina      # atualiza a página atual
    st.rerun()                            # recarrega a tela para refletir a mudança


# CABEÇALHO
col1, col2 = st.columns([4, 1])        # Cria duas colunas na tela (uma maior e uma menor)

with col2:              # Usa a segunda coluna
    st.markdown("👤 *Aluno*")         # mostra o texto com o emoji (podemos mudar depois para mostrar o nome do usuário - Falar com grupo 2)
 
st.divider()            # Linha divisória


# TELA: LISTA DE DESAFIOS
if st.session_state.pagina == 'lista':        # Verifica se a página atual é 'lista'

    st.write("### Lista de Desafios")         # título

    desafios = [       # Lista de desafios (fixa por enquanto, vamos mudar depois - falar com grupo 1)
        "Desafio 01 - Como conectar com Supabase",
        "Desafio 02 - Teste"
    ]

    for d in desafios:         # Percorre cada desafio da lista
 
        with st.container(border=True):       # Cria um bloco visual com borda
            st.write(f"### {d}")              # mostra o nome do desafio
            st.caption("em andamento")        # subtítulo

            if st.button(f"Acessar {d}"):           # Cria um botão para acessar o desafio
                st.session_state.desafio = d        # salva o desafio escolhido
                ir('votacao')                       # muda para a tela de votação

    st.divider()

    if st.button("Ver votos cadastrados"):          # Botão para ir na tela de visualização de votos
        ir('visualizar')


# TELA: VOTAÇÃO
elif st.session_state.pagina == 'votacao':
  
    if st.button("← Voltar", key="btn_voltar_votacao"):  # Botão para voltar (com 'key' única para evitar erro de widget duplicado no Streamlit)
        ir('lista')

    desafio = st.session_state.desafio       # Pega o desafio selecionado

    st.write(f"### {desafio} | Votação")     # Mostra o título da votação

    # 1. Buscar todos os votos para fazer a verificação
    dados = listar_votos()                   # Busca os dados no banco para verificação
    ja_votou = False                         # Variável de controle começando como falsa
    
    if dados.data:                           # Se houver dados cadastrados no banco
        df = pd.DataFrame(dados.data)        # Converte em tabela
        
        # 2. Filtrar se existe o ID do usuário para este desafio específico
        filtro = df[(df["usuario"] == st.session_state.id_usuario) & (df["desafio"] == desafio)]
        
        if not filtro.empty:                 # Se o filtro não estiver vazio, o usuário já votou aqui
            ja_votou = True                  # Muda o status de controle para verdadeiro

    # 3. Travar a tela se já tiver votado
    if ja_votou:
        st.warning("⚠️ Você já registrou um voto para este desafio!")   # Esconde o form e mostra o aviso
    
    else:
        # Se não votou, exibe as opções normalmente
        voto = st.radio("Escolha sua nota:", ["Bom", "Regular", "Ruim"])      # Cria opções de voto

        if st.button("Enviar Voto"):             # Botão para enviar voto
            try:
                inserir_voto(st.session_state.id_usuario, desafio, voto)  # Salva o voto usando o ID do usuário da sessão

                st.success("Voto salvo com sucesso")             # Mensagem de sucesso
                st.session_state.desafio = None                  # Limpa o desafio selecionado
                ir('lista')                                      # Volta para a lista

            except Exception as e:
                st.error(f"Erro ao salvar: {e}")                 # Se der erro, mostra na tela


# TELA: VISUALIZAR VOTOS
elif st.session_state.pagina == 'visualizar':

    if st.button("← Voltar", key="btn_voltar_visualizar"):   # Botão para voltar (com 'key' única)
        ir('lista')

    st.write("### Votos cadastrados")    # título

    dados = listar_votos()               # Busca os votos no banco

    if dados.data:                       # Verifica se existem dados

        df = pd.DataFrame(dados.data)    # Converte os dados em tabela

        st.write(df)                     # Mostra a tabela na tela

        st.divider()

        
        # GRÁFICO GERAL
  
        st.write("### Resultado Geral")

        contagem = df["voto"].value_counts()            # Conta quantos votos existem de cada tipo

        contagem = contagem.reindex(["Bom", "Regular", "Ruim"], fill_value=0)        # Garante que todas as opções apareçam (mesmo com 0 votos)

        st.bar_chart(contagem)                          # Mostra gráfico de barras

        st.divider()
        

        # GRÁFICO POR DESAFIO

        desafios_unicos = df["desafio"].unique()        # Pega os desafios únicos

        desafio_selecionado = st.selectbox(             # Caixa de seleção para escolher o desafio
            "Filtrar por desafio",
            desafios_unicos
        )

        df_filtrado = df[df["desafio"] == desafio_selecionado]         # Filtra a tabela pelo desafio escolhido

        st.write(f"### Resultado - {desafio_selecionado}")

        contagem_filtrada = df_filtrado["voto"].value_counts()         # Conta votos do desafio filtrado

        contagem_filtrada = contagem_filtrada.reindex(["Bom", "Regular", "Ruim"], fill_value=0)        # Garante todas as opções

        st.bar_chart(contagem_filtrada)           # Mostra gráfico

        st.divider()


        # EDITAR / EXCLUIR

        id_voto = st.number_input("Digite o ID do voto", step=1)        # Campo para digitar o ID do voto

        if st.button("Editar / Excluir"):                               # Botão para ir para edição
            st.session_state.voto_id = id_voto                          # salva o ID
            ir('editar')                                                # vai para a tela de edição

    else:
        st.info("Nenhum voto encontrado")                               # Caso não tenha dados


# TELA: EDITAR / EXCLUIR
elif st.session_state.pagina == 'editar':

    if st.button("← Voltar", key="btn_voltar_editar"):      # Botão de voltar (com 'key' única)
        ir('visualizar')

    id_voto = st.session_state.voto_id      # Recupera o ID salvo

    dados = buscar_voto_por_id(id_voto)     # Busca o voto no banco

    if dados.data:                          # Verifica se encontrou o voto

        voto_atual = dados.data[0]["voto"]                        # Pega o voto atual

        desafio = dados.data[0]["desafio"]                        # Pega o desafio

        st.write(f"### {desafio} | Editar voto ID {id_voto}")      # Mostra título

        novo_voto = st.radio(             # Radio já selecionado com o valor atual
            "Novo voto:",
            ["Bom", "Regular", "Ruim"],
            index=["Bom", "Regular", "Ruim"].index(voto_atual)
        )

        col1, col2 = st.columns(2)        # Cria duas colunas

        with col1:                                               # Coluna de atualizar
            if st.button("Atualizar"):
                atualizar_voto(id_voto, novo_voto)       # atualiza no banco
                st.success("Voto atualizado")

        with col2:                                               # Coluna de excluir
            if st.button("Excluir"):
                deletar_voto(id_voto)                    # remove do banco
                st.success("Voto excluído")

    else: 
        st.error("Voto não encontrado")                 # Caso não encontre o voto
