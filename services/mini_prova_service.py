from database.conexao import supabase


def buscar_professor_por_email(email):

    resposta = (
        supabase
        .table("professores")
        .select("*")
        .eq("email", email)
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
        .insert({
            "nome": nome
        })
        .execute()
    )

    return criar.data[0]


def buscar_ou_criar_tema(
    disciplina_id,
    nome
):

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

    professor = buscar_professor_por_email(
        dados["email_professor"]
    )

    disciplina = buscar_ou_criar_disciplina(
        dados["disciplina"]
    )

    tema = buscar_ou_criar_tema(
        disciplina["id"],
        dados["assunto"]
    )

    questao = (
        supabase
        .table("questoes")
        .insert({
            "professor_id": professor["id"],
            "disciplina_id": disciplina["id"],
            "tema_id": tema["id"],
            "tipo": "multipla_escolha",
            "nivel": dados["nivel"],
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

        supabase.table(
            "alternativas"
        ).insert({
            "questao_id": questao_id,
            "texto": alternativas[i],
            "correta": (
                letras[i]
                == dados["resposta_correta"]
            ),
            "ordem": i + 1
        }).execute()


def criar_mini_prova(dados):

    professor = buscar_professor_por_email(
        dados["email_professor"]
    )

    disciplina = buscar_ou_criar_disciplina(
        dados["disciplina"]
    )

    resposta = (
        supabase
        .table("mini_provas")
        .insert({
            "professor_id": professor["id"],
            "disciplina_id": disciplina["id"],
            "titulo": dados["titulo"],
            "descricao": dados["assunto"],
            "qtde_questoes": dados["quantidade_total"],
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
        .select("""
            id,
            enunciado,
            nivel,
            disciplinas(nome),
            temas(nome)
        """)
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


def atualizar_pergunta(
    id_pergunta,
    dados
):

    supabase.table(
        "questoes"
    ).update({
        "enunciado": dados["enunciado"],
        "nivel": dados["nivel"]
    }).eq(
        "id",
        id_pergunta
    ).execute()


def excluir_pergunta(id_pergunta):

    supabase.table(
        "questoes"
    ).delete().eq(
        "id",
        id_pergunta
    ).execute()


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


def atualizar_mini_prova(
    id_mini_prova,
    dados
):

    supabase.table(
        "mini_provas"
    ).update({
        "titulo": dados["titulo"],
        "descricao": dados["descricao"],
        "qtde_questoes": dados["qtde_questoes"],
        "duracao_minutos": dados["duracao_minutos"]
    }).eq(
        "id",
        id_mini_prova
    ).execute()


def excluir_mini_prova(id_mini_prova):

    supabase.table(
        "mini_provas"
    ).delete().eq(
        "id",
        id_mini_prova
    ).execute()
