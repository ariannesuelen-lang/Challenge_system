from database.conexao import supabase


def listar_desafios_votacao():

    resposta = (
        supabase
        .table("tela_desafio")
        .select("*")
        .execute()
    )

    return resposta.data


def registrar_voto(usuario, desafio, voto):

    verificar = (
        supabase
        .table("votos")
        .select("*")
        .eq("usuario", usuario)
        .eq("desafio", desafio)
        .execute()
    )

    if verificar.data:

        return False

    (
        supabase
        .table("votos")
        .insert({
            "usuario": usuario,
            "desafio": desafio,
            "voto": voto
        })
        .execute()
    )

    return True


def listar_votos():

    resposta = (
        supabase
        .table("votos")
        .select("*")
        .execute()
    )

    return resposta.data
