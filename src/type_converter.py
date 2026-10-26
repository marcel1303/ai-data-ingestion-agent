
def converter_quantidade(registro):
    novo_registro = registro.copy()

    novo_registro["quantity"] = int(
        novo_registro["quantity"]
    )

    return novo_registro
