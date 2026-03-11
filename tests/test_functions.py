import pytest
from unittest.mock import patch, MagicMock
from functions import (
    iterate_and_multiply_keys,
    pick_products,
    is_exit_key,
    get_build_quantity,
    is_user_input_in_map,
    calculate_total_basic_resources,
    calculate_total_resources,
    sum_resources_from_each_product,
    get_materials
)
def _make_cyclic_map() -> dict:
    """Build a materials map with a circular dependency for recursion-limit tests.

    CyclicA → CyclicB → CyclicA → … (infinite loop without a depth guard).
    Each class's total_basic_resources uses this same map so depth is propagated.
    """
    local_map: dict = {}

    class CyclicA:
        @classmethod
        def total_basic_resources(cls, depth: int = 0) -> dict:
            return calculate_total_basic_resources({"CyclicB": 1.0}, local_map, depth)

    class CyclicB:
        @classmethod
        def total_basic_resources(cls, depth: int = 0) -> dict:
            return calculate_total_basic_resources({"CyclicA": 1.0}, local_map, depth)

    local_map["CyclicA"] = CyclicA
    local_map["CyclicB"] = CyclicB
    return local_map


@pytest.mark.parametrize("key, expected", [("Salvage", 22.0), ("Coal", 10.0)])
def test_iterate_and_multiply_keys_values(key: str, expected: float) -> None:
    resource_costs = {"Salvage": 10.0, "Coal": 5.0}
    accumulated = {"Salvage": 2.0}
    qty = 2

    output = iterate_and_multiply_keys(resource_costs, accumulated, qty)

    assert output[key] == expected

def test_iterate_and_multiply_keys_length() -> None:
    resource_costs = {"Salvage": 10.0, "Coal": 5.0}
    accumulated = {"Salvage": 2.0}
    qty = 2
    output = iterate_and_multiply_keys(resource_costs, accumulated, qty)
    assert len(output) == 2

def test_iterate_and_multiply_keys_empty_map() -> None:
    resource_costs: dict[str, float] = {}
    accumulated = {"Sulfur": 1.0}
    qty = 5
    output = iterate_and_multiply_keys(resource_costs, accumulated, qty)
    assert output == {"Sulfur": 1.0}


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


def test_is_exit_key_true() -> None:
    assert is_exit_key("done") is True

def test_is_exit_key_false() -> None:
    assert is_exit_key("exit") is False
    assert is_exit_key("Done") is False  # Case sensitive based on implementation


def test_get_build_quantity_valid_int() -> None:
    with patch('builtins.input', return_value="5"):
        assert get_build_quantity("Outlaw") == 5

def test_get_build_quantity_invalid_then_valid() -> None:
    # First input "abc" (raises ValueError), second input "10" (valid)
    with patch('builtins.input', side_effect=["abc", "10"]):
        assert get_build_quantity("Chieftain") == 10


def test_is_user_input_in_map() -> None:
    products_map = {"Outlaw": 1, "Chieftain": 2}
    assert is_user_input_in_map("Outlaw", products_map) is True
    assert is_user_input_in_map("Silverhand", products_map) is False


@pytest.mark.parametrize("resource, expected_amount", [("Salvage", 20.0), ("Coal", 10.0)])
def test_calculate_total_resources(resource: str, expected_amount: float) -> None:
    mock_outlaw = MagicMock()
    mock_outlaw.total_basic_resources.return_value = {"Salvage": 10.0, "Coal": 5.0}

    products_map = {"Outlaw": mock_outlaw}
    user_selection = [("Outlaw", 2)]

    total = calculate_total_resources(user_selection, products_map)

    assert total[resource] == expected_amount

def test_calculate_total_resources_no_method() -> None:
    class ProductWithoutResources: pass

    products_map = {"InvalidProduct": ProductWithoutResources()}
    user_selection = [("InvalidProduct", 1)]

    total = calculate_total_resources(user_selection, products_map)
    assert total == {}


@pytest.mark.parametrize("resource, expected", [("Salvage", 15.0), ("Sulfur", 20.0)])
def test_sum_resources_from_each_product(resource: str, expected: float) -> None:
    resource_costs = {"Salvage": 10.0, "Sulfur": 20.0}
    accumulated = {"Salvage": 5.0}
    
    sum_resources_from_each_product(resource_costs, accumulated)

    assert accumulated[resource] == expected


@pytest.mark.parametrize("material, expected", [("PCmat", 15.0), ("A1", 30.0)])
def test_get_materials(material: str, expected: float) -> None:
    mock_chieftain = MagicMock()
    mock_chieftain.cost = {"PCmat": 5.0, "A1": 10.0}

    products_map = {"Chieftain": mock_chieftain}
    user_selection = [("Chieftain", 3)]
    
    total = get_materials(user_selection, products_map)

    assert total[material] == expected

def test_get_materials_no_cost() -> None:
    class ProductWithoutCost: pass
    products_map = {"InvalidProduct": ProductWithoutCost()}
    user_selection = [("InvalidProduct", 1)]

    total = get_materials(user_selection, products_map)
    assert total == {}


# === Recursion safety limit tests ===

def test_recursion_limit_raises_error() -> None:
    """Circular dependency in materials_map must raise RecursionError."""
    cyclic_map = _make_cyclic_map()
    with pytest.raises(RecursionError):
        calculate_total_basic_resources({"CyclicA": 1.0}, cyclic_map)

def test_recursion_limit_error_message() -> None:
    """RecursionError message must mention depth or circular dependencies."""
    cyclic_map = _make_cyclic_map()
    with pytest.raises(RecursionError, match="circular|depth exceeded"):
        calculate_total_basic_resources({"CyclicA": 1.0}, cyclic_map)

def test_calculate_total_resources_handles_recursion_error(capsys) -> None:
    """calculate_total_resources must skip a product that causes RecursionError and print an error."""
    mock_product = MagicMock()
    mock_product.total_basic_resources.side_effect = RecursionError(
        "Recursion depth exceeded (>10). Check products.json or materials.py for circular dependencies."
    )

    products_map = {"BrokenProduct": mock_product}
    user_selection = [("BrokenProduct", 1)]

    total = calculate_total_resources(user_selection, products_map)

    assert total == {}
    captured = capsys.readouterr()
    assert "Error" in captured.out
    assert "BrokenProduct" in captured.out
