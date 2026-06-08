from database.conexao import supabase


def buscar_professor_por_email(email):
    # Correção: A tabela real é 'usuarios', filtrando pelo tipo correto
    resposta = (
        supabase
        .table("usuarios")
        .select("*")
        .eq("email", email)
        .eq("tipo_usuario", "professor")
        .execute()
    )

    if resposta.data:
        return resposta.data[0]

    return None


def buscar_ou_criar_disciplina(nome):
    buscar = (
        supabase
        .table("disciplinas")
        .select("*")
        .eq("nome", nome)
        .execute()
    )

    if buscar.data:
        return buscar.data[0]

    criar = (
        supabase
        .table("disciplinas")
        .insert({"nome": nome})
        .execute()
    )

    return criar.data[0]


def buscar_ou_criar_tema(disciplina_id, nome):
    buscar = (
        supabase
        .table("temas")
        .select("*")
        .eq("nome", nome)
        .eq("disciplina_id", disciplina_id)
        .execute()
    )

    if buscar.data:
        return buscar.data[0]

    criar = (
        supabase
        .table("temas")
        .insert({
            "nome": nome,
            "disciplina_id": disciplina_id
        })
        .execute()
    )

    return criar.data[0]


def criar_pergunta(dados):
    professor = buscar_professor_por_email(dados["email_professor"])
    disciplina = buscar_ou_criar_disciplina(dados["disciplina"])
    tema = buscar_ou_criar_tema(disciplina["id"], dados["assunto"])

    # Correções: colunas 'professor_id' (usa usuario_uuid), 'tipo_questao' e 'nivel_dificuldade'
    questao = (
        supabase
        .table("questoes")
        .insert({
            "professor_id": professor["usuario_uuid"],  # FK aponta para usuario_uuid
            "disciplina_id": disciplina["id"],
            "tema_id": tema["id"],
            "tipo_questao": "multipla_escolha",         # Corrigido de 'tipo'
            "nivel_dificuldade": dados["nivel"],        # Corrigido de 'nivel'
            "enunciado": dados["enunciado"],
            "pontos": 1
        })
        .execute()
    )

    questao_id = questao.data[0]["id"]

    alternativas = [
        dados["alternativa_a"],
        dados["alternativa_b"],
        dados["alternativa_c"],
        dados["alternativa_d"],
        dados["alternativa_e"]
    ]

    letras = ["A", "B", "C", "D", "E"]

    for i in range(5):
        # Correção: coluna 'ordem_exibicao'
        supabase.table("alternativas").insert({
            "questao_id": questao_id,
            "texto": alternativas[i],
            "correta": (letras[i] == dados["resposta_correta"]),
            "ordem_exibicao": i + 1                     # Corrigido de 'ordem'
        }).execute()


def criar_mini_prova(dados):
    professor = buscar_professor_por_email(dados["email_professor"])
    disciplina = buscar_ou_criar_disciplina(dados["disciplina"])

    # Correções: colunas 'professor_id' (usuario_uuid) e 'quantidade_questoes'
    resposta = (
        supabase
        .table("mini_provas")
        .insert({
            "professor_id": professor["usuario_uuid"],  # FK aponta para usuario_uuid
            "disciplina_id": disciplina["id"],
            "titulo": dados["titulo"],
            "descricao": dados["assunto"],
            "quantidade_questoes": dados["quantidade_total"],  # Corrigido de 'qtde_questoes'
            "duracao_minutos": dados["tempo_minutos"],
            "status": "rascunho"
        })
        .execute()
    )

    return resposta.data


def listar_mini_provas():
    resposta = (
        supabase
        .table("mini_provas")
        .select("*")
        .execute()
    )
    return resposta.data


def listar_perguntas():
    resposta = (
        supabase
        .table("questoes")
        .select("*")
        .execute()
    )
    return resposta.data


def buscar_pergunta(id_pergunta):
    resposta = (
        supabase
        .table("questoes")
        .select("*")
        .eq("id", id_pergunta)
        .execute()
    )

    if resposta.data:
        return resposta.data[0]

    return None


def atualizar_pergunta(id_pergunta, dados):
    # Correção: coluna 'nivel_dificuldade'
    supabase.table("questoes").update({
        "enunciado": dados["enunciado"],
        "nivel_dificuldade": dados["nivel"]  # Corrigido de 'nivel'
    }).eq("id", id_pergunta).execute()


def excluir_pergunta(id_pergunta):
    supabase.table("questoes").delete().eq("id", id_pergunta).execute()


def buscar_mini_prova(id_mini_prova):
    resposta = (
        supabase
        .table("mini_provas")
        .select("*")
        .eq("id", id_mini_prova)
        .execute()
    )

    if resposta.data:
        return resposta.data[0]

    return None


def atualizar_mini_prova(id_mini_prova, dados):
    # Correção: coluna 'quantidade_questoes'
    supabase.table("mini_provas").update({
        "titulo": dados["titulo"],
        "descricao": dados["descricao"],
        "quantidade_questoes": dados["qtde_questoes"],  # Corrigido de 'qtde_questoes'
        "duracao_minutos": dados["duracao_minutos"]
    }).eq("id", id_mini_prova).execute()


def excluir_mini_prova(id_mini_prova):
    supabase.table("mini_provas").delete().eq("id", id_mini_prova).execute()
