
import csv


def extrair_colunas_csv(caminho_arquivo):
    with open(caminho_arquivo, mode="r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.reader(arquivo)

        for linha in leitor:
            if linha and any(coluna.strip() for coluna in linha):
                return linha

    raise ValueError("O arquivo CSV não possui um cabeçalho válido.")


def ler_registros_csv(caminho_arquivo):
    with open(caminho_arquivo, mode="r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(
            linha for linha in arquivo if linha.strip()
        )

        registros = list(leitor)

    return registros