import pytest
from unittest.mock import patch, MagicMock
from functions import (
    iterate_and_multiply_keys,
    pick_products,
    is_exit_key,
    get_build_quantity,
    is_user_input_in_map,
    calculate_total_resources,
    sum_resources_from_each_product,
    get_materials
)

# Test iterate_and_multiply_keys
def test_iterate_and_multiply_keys() -> None:
    # Setup
    resource_costs = {"Salvage": 10.0, "Coal": 5.0}
    accumulated = {"Salvage": 2.0}
    qty = 2

    # Execute
    output = iterate_and_multiply_keys(resource_costs, accumulated, qty)

    # Assert
    # Salvage: 2.0 + 10.0 * 2 = 22.0
    # Coal: 0.0 + 5.0 * 2 = 10.0
    assert output["Salvage"] == 22.0
    assert output["Coal"] == 10.0
    assert len(output) == 2

def test_iterate_and_multiply_keys_empty_map() -> None:
    resource_costs: dict[str, float] = {}
    accumulated = {"Sulfur": 1.0}
    qty = 5
    output = iterate_and_multiply_keys(resource_costs, accumulated, qty)
    assert output == {"Sulfur": 1.0}

# Test pick_products
def test_pick_products_valid_key() -> None:
    options = ["Outlaw", "Chieftain"]
    lowercase_map = {"outlaw": "Outlaw", "chieftain": "Chieftain"}
    with patch('builtins.input', return_value="Outlaw"):
        result = pick_products(options, lowercase_map)
        assert result == "Outlaw"

def test_pick_products_case_insensitive() -> None:
    options = ["Outlaw"]
    lowercase_map = {"outlaw": "Outlaw"}
    with patch('builtins.input', return_value="oUtLaW"):
        result = pick_products(options, lowercase_map)
        assert result == "Outlaw"

def test_pick_products_invalid_key() -> None:
    options = ["Outlaw"]
    lowercase_map = {"outlaw": "Outlaw"}
    with patch('builtins.input', return_value="Silverhand"):
        result = pick_products(options, lowercase_map)
        assert result == "Silverhand"  # Returns input as is if not found

# Test is_exit_key
def test_is_exit_key_true() -> None:
    assert is_exit_key("done") is True

def test_is_exit_key_false() -> None:
    assert is_exit_key("exit") is False
    assert is_exit_key("Done") is False  # Case sensitive based on implementation

# Test get_build_quantity
def test_get_build_quantity_valid_int() -> None:
    with patch('builtins.input', return_value="5"):
        assert get_build_quantity("Outlaw") == 5

def test_get_build_quantity_invalid_then_valid() -> None:
    # First input "abc" (raises ValueError), second input "10" (valid)
    with patch('builtins.input', side_effect=["abc", "10"]):
        assert get_build_quantity("Chieftain") == 10

# Test is_user_input_in_map
def test_is_user_input_in_map() -> None:
    products_map = {"Outlaw": 1, "Chieftain": 2}
    assert is_user_input_in_map("Outlaw", products_map) is True
    assert is_user_input_in_map("Silverhand", products_map) is False

# Test calculate_total_resources
def test_calculate_total_resources() -> None:
    # Setup mock Outlaw that returns basic resources
    mock_outlaw = MagicMock()
    mock_outlaw.total_basic_resources.return_value = {"Salvage": 10.0, "Coal": 5.0}

    products_map = {"Outlaw": mock_outlaw}
    user_selection = [("Outlaw", 2)]

    # Execute
    total = calculate_total_resources(user_selection, products_map)

    # Assert
    # Salvage: 10 * 2 = 20
    # Coal: 5 * 2 = 10
    assert total["Salvage"] == 20.0
    assert total["Coal"] == 10.0

def test_calculate_total_resources_no_method() -> None:
    # Setup product without total_basic_resources method
    class ProductWithoutResources: pass

    products_map = {"InvalidProduct": ProductWithoutResources()}
    user_selection = [("InvalidProduct", 1)]

    total = calculate_total_resources(user_selection, products_map)
    assert total == {}

# Test sum_resources_from_each_product
def test_sum_resources_from_each_product() -> None:
    resource_costs = {"Salvage": 10.0, "Sulfur": 20.0}
    accumulated = {"Salvage": 5.0}

    # Execute
    sum_resources_from_each_product(resource_costs, accumulated)

    # Assert
    assert accumulated["Salvage"] == 15.0  # 5 + 10
    assert accumulated["Sulfur"] == 20.0  # 0 + 20

# Test get_materials
def test_get_materials() -> None:
    # Setup mock Chieftain with facility material costs
    mock_chieftain = MagicMock()
    mock_chieftain.cost = {"PCmat": 5.0, "A1": 10.0}

    products_map = {"Chieftain": mock_chieftain}
    user_selection = [("Chieftain", 3)]

    # Execute
    total = get_materials(user_selection, products_map)

    # Assert
    # PCmat: 5.0 * 3 = 15.0
    # A1: 10.0 * 3 = 30.0
    assert total["PCmat"] == 15.0
    assert total["A1"] == 30.0

def test_get_materials_no_cost() -> None:
    class ProductWithoutCost: pass
    products_map = {"InvalidProduct": ProductWithoutCost()}
    user_selection = [("InvalidProduct", 1)]

    total = get_materials(user_selection, products_map)
    assert total == {}
