from database.conexao import supabase


def listar_mini_provas():

    resposta = (
        supabase
        .table("mini_provas")
        .select("*")
        .execute()
    )

    return resposta.data
