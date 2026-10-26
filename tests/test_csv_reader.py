
import sys
import pytest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from csv_reader import extrair_colunas_csv, ler_registros_csv


def test_extrair_colunas_csv(tmp_path):
    caminho = tmp_path / "vendas.csv"

    caminho.write_text(
        "\nID_CLIENTE,DT,ITEM,QTD,PRECO_UN\n"
        "101,2026-10-01,Notebook,2,3500.00\n",
        encoding="utf-8"
    )

    resultado = extrair_colunas_csv(caminho)

    assert resultado == [
        "ID_CLIENTE",
        "DT",
        "ITEM",
        "QTD",
        "PRECO_UN"
    ]


def test_extrair_colunas_csv_vazio(tmp_path):
    caminho = tmp_path / "vazio.csv"

    caminho.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="não possui um cabeçalho válido"):
        extrair_colunas_csv(caminho)

        
def test_ler_registros_csv(tmp_path):
    caminho = tmp_path / "vendas.csv"

    caminho.write_text(
        "\nID_CLIENTE,DT,ITEM,QTD,PRECO_UN\n"
        "101,2026-10-01,Notebook,2,3500.00\n"
        "102,2026-10-02,Mouse,5,85.90\n",
        encoding="utf-8"
    )

    registros = ler_registros_csv(caminho)

    assert len(registros) == 2

    assert registros[0] == {
        "ID_CLIENTE": "101",
        "DT": "2026-10-01",
        "ITEM": "Notebook",
        "QTD": "2",
        "PRECO_UN": "3500.00"
    }

    assert registros[1]["ITEM"] == "Mouse"