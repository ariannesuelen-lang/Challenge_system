def usuario_e_admin(usuario):

    if not usuario:
        return False

    return usuario["tipo_usuario"] == "admin"
