import hashlib
import re

from database.conexao import supabase

def criptografar_senha(senha):

    return hashlib.sha256(
        senha.encode()
    ).hexdigest()

def senha_valida(senha):

    if len(senha) < 8:
        return "A senha deve ter no mínimo 8 caracteres"

    if not re.search(r"[A-Z]", senha):
        return "A senha deve conter letra maiúscula"

    if not re.search(r"\d", senha):
        return "A senha deve conter número"

    return "ok"


def login_usuario(email, senha):

    resposta = (
        supabase
        .table("usuarios")
        .select("*")
        .eq("email", email)
        .eq("senha", criptografar_senha(senha))
        .execute()
    )

    if resposta.data:
        return resposta.data[0]

    return None


def cadastrar_usuario(
    nome,
    email,
    tipo_usuario,
    senha
):

    validar = senha_valida(senha)

    if validar != "ok":
        return validar

    verificar = (
        supabase
        .table("usuarios")
        .select("id")
        .eq("email", email)
        .execute()
    )

    if verificar.data:
        return "E-mail já cadastrado"

    resposta_usuario = (
        supabase
        .table("usuarios")
        .insert({
            "nome": nome,
            "email": email,
            "tipo_usuario": tipo_usuario,
            "senha": criptografar_senha(senha)
        })
        .execute()
    )

    if tipo_usuario == "professor":

        supabase.table(
            "professores"
        ).insert({
            "nome": nome,
            "email": email
        }).execute()

    elif tipo_usuario == "aluno":

        supabase.table(
            "alunos"
        ).insert({
            "nome": nome,
            "email": email
        }).execute()

    return "ok"
