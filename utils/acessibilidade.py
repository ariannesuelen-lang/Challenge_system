from database.conexao import supabase


def listar_mini_provas():

    return supabase.table(
        "mini_provas"
    ).select("*").execute()