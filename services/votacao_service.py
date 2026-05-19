from database.conexao import supabase


def listar_desafios_votacao():

    resposta = (
        supabase
        .table("tela_desafio")
        .select("*")
        .execute()
    )

    return resposta.data


def registrar_voto(usuario_id, desafio_id, nota):

    verificar = (
        supabase
        .table("votos")
        .select("*")
        .eq("usuario_id", usuario_id)
        .eq("desafio_id", desafio_id)
        .execute()
    )

    if verificar.data:
        return False

    (
        supabase
        .table("votos")
        .insert({
            "usuario_id": usuario_id,
            "desafio_id": desafio_id,
            "nota": nota
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
