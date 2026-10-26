
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from transformer import aplicar_mapeamento


def test_aplicar_mapeamento():
    registros = [
        {"ID_CLIENTE": "101", "ITEM": "Notebook"},
        {"ID_CLIENTE": "102", "ITEM": "Mouse"}
    ]

    mapeamento = {
        "ID_CLIENTE": "customer_id",
        "ITEM": "product"
    }

    resultado = aplicar_mapeamento(registros, mapeamento)

    assert resultado == [
        {"customer_id": "101", "product": "Notebook"},
        {"customer_id": "102", "product": "Mouse"}
    ]


def test_aplicar_mapeamento_coluna_inexistente():
    registros = [
        {"ID_CLIENTE": "101"}
    ]

    mapeamento = {
        "ID_CLIENTE": "customer_id",
        "ITEM": "product"
    }

    with pytest.raises(KeyError):
        aplicar_mapeamento(registros, mapeamento)
