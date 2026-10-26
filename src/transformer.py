
def aplicar_mapeamento(registros, mapeamento):
    registros_transformados = []

    for registro in registros:
        novo_registro = {}

        for coluna_origem, coluna_destino in mapeamento.items():
            novo_registro[coluna_destino] = registro[coluna_origem]

        registros_transformados.append(novo_registro)

    return registros_transformados
