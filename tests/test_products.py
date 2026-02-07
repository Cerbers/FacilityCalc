import pytest
import json
from unittest.mock import patch, mock_open
import products
from products import Prod, _load_products

def test_prod_empty_cost_exception() -> None:
    """Test that calculating resources for a Prod with empty cost raises ValueError."""
    class EmptyProduct(Prod):
        cost = {}
        faction = "warden"
        
    with pytest.raises(ValueError, match="No attributes in cost dictionary in EmptyProduct"):
        EmptyProduct.total_basic_resources()

def test_prod_class_method() -> None:
    """Test the base Prod class functionality using a dummy subclass."""
    class TestProduct(Prod):
        cost = {
            "Cmat": 10.0,
            "A4": 2.0
        }
        faction = "warden"
        
    resources = TestProduct.total_basic_resources()
    assert resources["Salvage"] == 250.0

def test_prod_invalid_faction() -> None:
    """Test that defining a Prod subclass with invalid faction raises ValueError."""
    with pytest.raises(ValueError, match="Invalid faction 'invalid' for product 'InvalidProduct'"):
        class InvalidProduct(Prod):
            cost = {"Cmat": 10.0}
            faction = "invalid"


def test_load_products_success() -> None:
    """Test that products are loaded correctly from JSON."""
    data = {
        "TestVehicle": {
            "cost": {
                "Cmat": 10.0,
                "A4": 5.0
            },
            "faction": "warden"
        }
    }
    mock_json = json.dumps(data)
    
    with patch("builtins.open", mock_open(read_data=mock_json)):
        with patch("json.load", return_value=data):
            _load_products()
            
            assert hasattr(products, "TestVehicle")
            VehicleClass = getattr(products, "TestVehicle")
            assert issubclass(VehicleClass, Prod)
            assert VehicleClass.cost == {"Cmat": 10.0, "A4": 5.0}
            assert VehicleClass.faction == "warden"

            resources = VehicleClass.total_basic_resources()

            assert resources["Salvage"] == 550.0
            assert resources.get("Coal", 0.0) == 0.0

def test_load_products_file_not_found(capsys) -> None:
    """Test that FileNotFoundError is handled gracefully."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        _load_products()
        captured = capsys.readouterr()
        assert "Warning" in captured.out
        assert "No products loaded" in captured.out

def test_load_products_json_error(capsys) -> None:
    """Test that JSONDecodeError is handled gracefully."""
    with patch("builtins.open", mock_open(read_data="invalid")):
        with patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)):
            _load_products()
            captured = capsys.readouterr()
            assert "Error" in captured.out
            assert "Failed to decode" in captured.out
