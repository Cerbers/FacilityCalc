import pytest
import json
from unittest.mock import patch, mock_open
import products
from products import Prod, _load_products

def test_prod_empty_cost_exception() -> None:
    """Test that calculating resources for a Prod with empty cost raises ValueError."""
    class EmptyProduct(Prod):
        cost = {}
        
    with pytest.raises(ValueError, match="No attributies in cost dictionary in EmptyProduct"):
        EmptyProduct.total_basic_resources()

def test_prod_class_method() -> None:
    """Test the base Prod class functionality using a dummy subclass."""
    class TestProduct(Prod):
        cost = {
            "Cmat": 10.0,
            "A4": 2.0
        }
        
    resources = TestProduct.total_basic_resources()
    assert resources["Salvage"] == 250.0

def test_load_products_success() -> None:
    """Test that products are loaded correctly from JSON."""
    data = {
        "TestVehicle": {
            "Cmat": 10.0,
            "A4": 5.0
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
            
            # Verify resource calculation works on loaded class
            resources = VehicleClass.total_basic_resources()
            # Cmat(10) -> 10 * 5 Salvage = 50 Salvage
            # A4(5) -> 5 * (PCmat(1)) -> 5 * (Cmat(15) + Salvage(25)) -> 5 * (15*5 + 25) = 5 * 100 = 500 Salvage
            # Total: 550 Salvage, 0 Coal
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
