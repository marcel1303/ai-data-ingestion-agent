
import sys
from pathlib import Path

# Permite importar os módulos da pasta src
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from validators import (
    validar_coluna_origem,
    validar_coluna_destino,
    validar_destino_duplicado,
    identificar_colunas_nao_mapeadas,
    validar_mapeamento
)


def test_validar_coluna_origem():
    colunas_validas = ["ID_CLIENTE", "DT", "ITEM"]

    assert validar_coluna_origem("ID_CLIENTE", colunas_validas) is True
    assert validar_coluna_origem("COD_INEXISTENTE", colunas_validas) is False


def test_validar_coluna_destino():
    colunas_validas = [
        "customer_id",
        "sale_date",
        "product",
        "quantity",
        "unit_price"
    ]

    assert validar_coluna_destino("customer_id", colunas_validas) is True
    assert validar_coluna_destino("customer_name", colunas_validas) is False

def test_validar_destino_duplicado():
    destinos_utilizados = {"quantity", "product"}

    assert validar_destino_duplicado(
        "quantity", destinos_utilizados
    ) is True

    assert validar_destino_duplicado(
        "unit_price", destinos_utilizados
    ) is False

    
def test_identificar_colunas_nao_mapeadas():
    colunas_origem = [
        "ID_CLIENTE",
        "DT",
        "ITEM",
        "QTD",
        "PRECO_UN"
    ]

    mapeamento = {
        "ID_CLIENTE": "customer_id",
        "DT": "sale_date",
        "ITEM": "product",
        "QTD": "quantity"
    }

    resultado = identificar_colunas_nao_mapeadas(
        colunas_origem,
        mapeamento
    )

    assert resultado == {"PRECO_UN"}

def test_validar_mapeamento_completo():
    colunas_origem = ["ID_CLIENTE", "DT"]
    colunas_destino = ["customer_id", "sale_date"]

    mapeamento = {
        "ID_CLIENTE": "customer_id",
        "DT": "sale_date"
    }

    erros = validar_mapeamento(
        mapeamento,
        colunas_origem,
        colunas_destino
    )

    assert erros == []


def test_validar_mapeamento_invalido():
    colunas_origem = ["ID_CLIENTE", "DT"]
    colunas_destino = ["customer_id", "sale_date"]

    mapeamento = {
        "ID_CLIENTE": "customer_name",
        "DT": "sale_date"
    }

    erros = validar_mapeamento(
        mapeamento,
        colunas_origem,
        colunas_destino
    )

    assert erros == ["Destino inexistente: 'customer_name'"]