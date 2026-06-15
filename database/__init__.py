from .conexao import SupabaseConnection

# Expõe uma função direta e limpa para qualquer repositório obter o cliente do banco
def obter_client_banco():
    return SupabaseConnection.get_client()
