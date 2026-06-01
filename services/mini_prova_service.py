from database.conexao import supabase


def listar_mini_provas():

    resposta = (
        supabase
        .table("mini_provas")
        .select("*")
        .execute()
    )

    return resposta.data


def criar_mini_prova(dados):

    resposta = (
        supabase
        .table("mini_provas")
        .insert(dados)
        .execute()
    )

    return resposta.data


def criar_pergunta(dados):

    resposta = (
        supabase
        .table("questoes")
        .insert(dados)
        .execute()
    )

    return resposta.data
