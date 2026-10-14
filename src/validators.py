# Função para validar a existência da coluna de origem
def validar_coluna_origem(coluna, colunas_validas):
    return coluna in colunas_validas

# Função para validar a existência da coluna de destino
def validar_coluna_destino(coluna, colunas_validas):
    return coluna in colunas_validas

# Verifica se uma coluna de destino já foi utilizada
def validar_destino_duplicado(coluna, destinos_utilizados):
    return coluna in destinos_utilizados

# Identifica colunas de origem que não foram mapeadas
def identificar_colunas_nao_mapeadas(colunas_origem, mapeamento):
    return set(colunas_origem) - set(mapeamento.keys())

def validar_mapeamento(mapeamento, colunas_origem, colunas_destino):
    destinos_utilizados = set()
    erros = []

    for coluna_origem, coluna_destino in mapeamento.items():

        if not validar_coluna_origem(coluna_origem, colunas_origem):
            erros.append(f"Origem inexistente: {coluna_origem!r}")

        elif not validar_coluna_destino(coluna_destino, colunas_destino):
            erros.append(f"Destino inexistente: {coluna_destino!r}")

        elif validar_destino_duplicado(coluna_destino, destinos_utilizados):
            erros.append(f"Destino duplicado: {coluna_destino!r}")

        else:
            destinos_utilizados.add(coluna_destino)

    colunas_nao_mapeadas = identificar_colunas_nao_mapeadas(
        colunas_origem,
        mapeamento
    )

    for coluna in sorted(colunas_nao_mapeadas):
        erros.append(f"Coluna sem mapeamento: {coluna!r}")

    return erros