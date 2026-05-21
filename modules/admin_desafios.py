import streamlit as st
from conexao import inserir_desafio, listar_desafios, deletar_desafio, atualizar_desafio
from modules.utils import ir

def render():
    if st.button("← Voltar"):
        ir('lista')
        
    st.write("### ⚙️ Gerenciar Desafios")
    
    # Inicializa o estado de edição se não existir
    if 'editando_desafio' not in st.session_state:
        st.session_state.editando_desafio = None
    
    # Formulário para adicionar novo desafio
    novo_desafio = st.text_input("Nome do novo desafio:")
    if st.button("Adicionar Desafio"):
        if novo_desafio:
            inserir_desafio(novo_desafio)
            st.success("Desafio adicionado com sucesso!")
            st.rerun()
        else:
            st.warning("Por favor, digite um nome para o desafio.")
            
    st.divider()
    
    st.write("#### Desafios Cadastrados no Banco")
    resposta = listar_desafios()
    
    if resposta.data:
        for d in resposta.data:
            # Verifica se ESTE desafio é o que está sendo editado no momento
            if st.session_state.editando_desafio == d['id']:
                c1, c2, c3 = st.columns([3, 1, 1])
                
                # Campo de texto preenchido com o nome atual
                novo_nome = c1.text_input("Novo nome", value=d['nome'], key=f"input_{d['id']}", label_visibility="collapsed")
                
                if c2.button("💾 Salvar", key=f"save_{d['id']}"):
                    if novo_nome.strip() != "":
                        atualizar_desafio(d['id'], novo_nome)
                        st.session_state.editando_desafio = None
                        st.success("Desafio atualizado!")
                        st.rerun()
                    else:
                        st.warning("O nome não pode ficar vazio.")
                        
                if c3.button("❌ Cancelar", key=f"cancel_{d['id']}"):
                    st.session_state.editando_desafio = None
                    st.rerun()
            
            # Modo de visualização padrão
            else:
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.write(f"- {d['nome']}")
                
                if c2.button("✏️ Editar", key=f"edit_{d['id']}"):
                    st.session_state.editando_desafio = d['id']
                    st.rerun()
                    
                if c3.button("🗑️ Excluir", key=f"del_{d['id']}"):
                    deletar_desafio(d['id'])
                    st.rerun()
    else:
        st.info("Nenhum desafio no banco.")