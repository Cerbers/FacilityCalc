import builtins
from unittest.mock import patch
import pytest
from main import pick_products

test_strings = ["sdasdwda", "12312314"]
products = ["SPG, Outlaw, Thornfall"]

def test_pick_products(monkeypatch):
    # Simulate user input
    monkeypatch.setattr('builtins.input', lambda _: "SPG")
    result = pick_products()
    assert result == "SPG"

def test_pick_products_invalid(monkeypatch):
    # Simulate user input with a made-up value
    with pytest.raises(AssertionError):
        monkeypatch.setattr('builtins.input', lambda _: "NotAProduct")
        result = pick_products()
        assert result in products