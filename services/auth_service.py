import hashlib
import re

from database.conexao import supabase


def criptografar_senha(senha):
    """Cria um hash SHA-256 seguro a partir da senha em texto limpo."""
    return hashlib.sha256(
        senha.encode()
    ).hexdigest()


def senha_valida(senha):
    """Valida as regras de complexidade exigidas para a senha."""
    if len(senha) < 8:
        return "A senha deve ter no mínimo 8 caracteres"

    if not re.search(r"[A-Z]", senha):
        return "A senha deve conter letra maiúscula"

    if not re.search(r"\d", senha):
        return "A senha deve conter número"

    return "ok"


def login_usuario(email, senha):
    """Realiza a busca do usuário no banco com base no e-mail e hash da senha."""
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
    """Efetua o cadastro do novo usuário diretamente na tabela unificada."""
    try:
        # 1. Valida as regras de complexidade da senha
        validar = senha_valida(senha)
        if validar != "ok":
            return validar

        # 2. Verifica se o e-mail já existe na tabela única
        verificar = (
            supabase
            .table("usuarios")
            .select("id")
            .eq("email", email)
            .execute()
        )

        if verificar.data:
            return "E-mail já cadastrado"

        # 3. Insere o novo registro centralizado na tabela 'usuarios'
        supabase.table(
            "usuarios"
        ).insert({
            "nome": nome,
            "email": email,
            "tipo_usuario": tipo_usuario,
            "senha": criptografar_senha(senha)
        }).execute()

        # ✅ Correção: Removidos os espelhamentos para as tabelas antigas 'professores' e 'alunos'
        return "ok"

    except Exception as erro:
        return f"Erro ao cadastrar usuário: {erro}"