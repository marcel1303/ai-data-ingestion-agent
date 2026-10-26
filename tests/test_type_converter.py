
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from type_converter import converter_quantidade


def test_converter_quantidade():
    registro = {"quantity": "2"}

    resultado = converter_quantidade(registro)

    assert resultado["quantity"] == 2
    assert isinstance(resultado["quantity"], int)


def test_converter_quantidade_invalida():
    registro = {"quantity": "abc"}

    with pytest.raises(ValueError):
        converter_quantidade(registro)

