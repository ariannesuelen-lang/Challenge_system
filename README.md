# Challenge_system
MAIN
Sistema de Desafios - Universidades

> Fluxo de Navegação

O código utiliza o st.session_state para emular um sistema de múltiplas páginas em um único arquivo:
  °Estado lista: Exibe os desafios disponíveis.
  °Estado votacao: Exibe os detalhes e o formulário de notas do desafio selecionado.

> Componentes da Interface

Header: Layout de colunas para exibição de identificação do usuário (Aluno) e linha divisória persistente.
Navegação: Funções ir_para_votacao() e ir_para_lista() que alteram a variável de controle no session_state.
Container de Desafio: Card com borda contendo título, status (caption) e gatilho de navegação.
Área de Votação:
  °Expander: Seção retrátil para descrição detalhada e orientações de justificativa.
  °Checkboxes Lado a Lado: Organizados em 3 colunas para as notas Bom, Regular e Ruim.

