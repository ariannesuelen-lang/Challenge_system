from database.conexao import supabase


def listar_desafios_votacao():

    return [
        {
            "id": 1,
            "titulo": "Teste de Voto1",
            "descricao": "Apresentação teste 1",
            "prazo": "2026-12-31"
        },

        {
            "id": 2,
            "titulo": "Teste de Voto2",
            "descricao": "Apresentação teste 2",
            "prazo": "2026-12-31"
        }
    ]


def buscar_voto_usuario(usuario, desafio):

    resposta = (
        supabase
        .table("votos")
        .select("*")
        .eq("usuario", usuario)
        .eq("desafio", desafio)
        .execute()
    )

    if resposta.data:

        return resposta.data[0]

    return None


def registrar_voto(usuario, desafio, voto):

    verificar = buscar_voto_usuario(
        usuario,
        desafio
    )

    if verificar:

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


def atualizar_voto(id_voto, novo_voto):

    (
        supabase
        .table("votos")
        .update({
            "voto": novo_voto
        })
        .eq("id", id_voto)
        .execute()
    )


def listar_votos_desafio(desafio):

    resposta = (
        supabase
        .table("votos")
        .select("*")
        .eq("desafio", desafio)
        .execute()
    )

    return resposta.data
