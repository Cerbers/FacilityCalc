import pytest
from unittest.mock import patch, MagicMock
from functions import (
    iterate_and_multiply_keys,
    pick_products,
    is_exit_key,
    user_nums,
    is_user_input_in_map,
    calculate_total_resources,
    sum_resources_from_each_product,
    get_mats
)

# Test iterate_and_multiply_keys
def test_iterate_and_multiply_keys() -> None:
    # Setup
    data_map = {"a": 10.0, "b": 5.0}
    result = {"a": 2.0}
    qty = 2

    # Execute
    output = iterate_and_multiply_keys(data_map, result, qty)

    # Assert
    # a: 2.0 + 10.0 * 2 = 22.0
    # b: 0.0 + 5.0 * 2 = 10.0
    assert output["a"] == 22.0
    assert output["b"] == 10.0
    assert len(output) == 2

def test_iterate_and_multiply_keys_empty_map() -> None:
    data_map: dict[str, float] = {}
    result = {"a": 1.0}
    qty = 5
    output = iterate_and_multiply_keys(data_map, result, qty)
    assert output == {"a": 1.0}

# Test pick_products
def test_pick_products_valid_key() -> None:
    options = ["Car", "Bike"]
    data_map = {"car": "CarObject", "bike": "BikeObject"}
    with patch('builtins.input', return_value="Car"):
        result = pick_products(options, data_map)
        assert result == "CarObject"

def test_pick_products_case_insensitive() -> None:
    options = ["Car"]
    data_map = {"car": "CarObject"}
    with patch('builtins.input', return_value="cAr"):
        result = pick_products(options, data_map)
        assert result == "CarObject"

def test_pick_products_invalid_key() -> None:
    options = ["Car"]
    data_map = {"car": "CarObject"}
    with patch('builtins.input', return_value="Plane"):
        result = pick_products(options, data_map)
        assert result == "Plane"  # Returns input as is if not found

# Test is_exit_key
def test_is_exit_key_true() -> None:
    assert is_exit_key("done") is True

def test_is_exit_key_false() -> None:
    assert is_exit_key("exit") is False
    assert is_exit_key("Done") is False  # Case sensitive based on implementation

# Test user_nums
def test_user_nums_valid_int() -> None:
    with patch('builtins.input', return_value="5"):
        assert user_nums("Apples") == 5

def test_user_nums_invalid_then_valid() -> None:
    # First input "abc" (raises ValueError), second input "10" (valid)
    with patch('builtins.input', side_effect=["abc", "10"]):
        assert user_nums("Apples") == 10

# Test is_user_input_in_map
def test_is_user_input_in_map() -> None:
    data_map = {"key1": 1, "key2": 2}
    assert is_user_input_in_map("key1", data_map) is True
    assert is_user_input_in_map("key3", data_map) is False

# Test calculate_total_resources
def test_calculate_total_resources() -> None:
    # Setup
    mock_prod = MagicMock()
    mock_prod.total_basic_resources.return_value = {"Res1": 10.0, "Res2": 5.0}
    
    products_map = {"TestProd": mock_prod}
    user_selection = {"TestProd": 2}
    
    # Execute
    total = calculate_total_resources(user_selection, products_map)
    
    # Assert
    # Res1: 10 * 2 = 20
    # Res2: 5 * 2 = 10
    assert total["Res1"] == 20.0
    assert total["Res2"] == 10.0

def test_calculate_total_resources_no_method() -> None:
    # Setup product without total_basic_resources method
    mock_prod = MagicMock()
    del mock_prod.total_basic_resources # Ensure attribute doesn't exist if MagicMock created it
    # Actually MagicMock will create it on access unless spec is set or we explicitly delete it
    # Easier to just make an object that strictly doesn't have it, but strict typing expects objects
    # Let's use an empty class instance
    class Empty: pass
    
    products_map = {"EmptyProd": Empty()}
    user_selection = {"EmptyProd": 1}
    
    total = calculate_total_resources(user_selection, products_map)
    assert total == {}

# Test sum_resources_from_each_product
def test_sum_resources_from_each_product() -> None:
    data_map = {"A": 10.0, "B": 20.0}
    ref = {"A": 5.0}
    
    # Execute
    sum_resources_from_each_product(data_map, ref)
    
    # Assert
    assert ref["A"] == 15.0 # 5 + 10
    assert ref["B"] == 20.0 # 0 + 20

# Test get_mats
def test_get_mats() -> None:
    # Setup
    mock_prod = MagicMock()
    mock_prod.cost = {"Mat1": 2.0}
    
    products_map = {"TestProd": mock_prod}
    user_selection = {"TestProd": 3}
    
    # Execute
    total = get_mats(user_selection, products_map)
    
    # Assert
    # Mat1: 2.0 * 3 = 6.0
    assert total["Mat1"] == 6.0

def test_get_mats_no_cost() -> None:
    class Empty: pass
    products_map = {"EmptyProd": Empty()}
    user_selection = {"EmptyProd": 1}
    
    total = get_mats(user_selection, products_map)
    assert total == {}
