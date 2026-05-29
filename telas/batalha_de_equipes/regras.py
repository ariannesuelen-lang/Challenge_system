import streamlit as st


def tela_batalha_regras():

    st.title("Regras e Condutas")

    if st.button("Voltar"):
        st.session_state.pagina = "batalha_de_equipes"
        st.rerun()

    st.divider()

    st.subheader("Formato da Batalha")
    st.markdown("""
- O professor cria batalhas com titulo, descricao e prazo.
- Cada aluno envia uma resposta por batalha.
- O professor acompanha todas as respostas e finaliza a batalha quando necessario.
""")

    st.divider()

    st.subheader("Fair Play e Condutas")
    st.markdown("""
- E proibido copiar respostas de outros participantes.
- Comunicacao durante a batalha deve respeitar as regras definidas pelo professor.
- Todos os integrantes do time devem participar ativamente.
- Respeito mutuo e obrigatorio. Linguagem ofensiva pode gerar penalidade ou desclassificacao.
""")

    st.divider()

    st.subheader("Penalidades")
    st.markdown("""
| Infracao | Consequencia |
|---|---|
| Trapaca comprovada | Resposta invalidada |
| Conduta inadequada | Advertencia |
| Desrespeito | Exclusao da batalha |
| Nao participacao | Sem pontuacao na rodada |
""")

    st.divider()

    st.subheader("Ideologias")

    col1, col2 = st.columns(2)

    with col1:
        st.info("Colaboracao vs. Competicao Saudavel: competir sem perder o espirito de equipe.")
        st.info("Meritocracia com Equilibrio: pontuacao por desempenho e participacao.")

    with col2:
        st.info("Papeis no Time: lider, estrategista, apoio — cada um contribui.")
        st.info("Decisao sob Pressao: pensar rapido e em conjunto e a habilidade central.")
