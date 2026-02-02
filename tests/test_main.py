import pytest
from unittest.mock import patch, MagicMock
from typing import Type
import products
from products import Prod
from main import Products, lowercase_product_map, list_of_products


# Test Products dictionary
class TestProductsDictionary:
    @pytest.mark.parametrize("key", [
        "Outlaw", "Chieftain", "Thornfall", "Blinder", "Skycaller", "RAC",
        "King Jester", "Flame BT", "MG BT", "Stain SPG", "Storm Cannon", "Intel Center", "Underground Fortress",
        "RSC", "Warden Submarine", "Frigate", "Bluefin", "Longhook", "Bowhead", "Firebrand"
    ])
    def test_products_contains_all_vehicles(self, key: str) -> None:
        assert key in Products, f"Missing product: {key}"

    @pytest.mark.parametrize("name", [
        "Outlaw",
        "Chieftain",
        "Thornfall",
        "Blinder",
        "Skycaller",
        "RAC",
        "King Jester",
        "Flame BT",
        "MG BT",
        "Stain SPG",
        "Storm Cannon",
        "Intel Center",
        "Underground Fortress",
        "RSC",
        "Warden Submarine",
        "Frigate",
        "Bluefin",
        "Longhook",
        "Bowhead",
        "Firebrand",
    ])
    def test_products_maps_to_correct_classes(self, name: str) -> None:
        expected_class = getattr(products, name)
        assert Products[name] is expected_class

    @pytest.mark.parametrize("name, product_class", Products.items())
    def test_all_products_are_prod_subclasses(self, name: str, product_class: Type[Prod]) -> None:
        assert issubclass(product_class, Prod), f"{name} is not a Prod subclass"


# Test lowercase_product_map
class TestLowercaseProductMap:
    def test_lowercase_map_has_same_length_as_products(self) -> None:
        assert len(lowercase_product_map) == len(Products)

    @pytest.mark.parametrize("key", lowercase_product_map.keys())
    def test_lowercase_map_keys_are_lowercase(self, key: str) -> None:
        assert key == key.lower(), f"Key '{key}' is not lowercase"

    @pytest.mark.parametrize("lowercase_key, original_key", lowercase_product_map.items())
    def test_lowercase_map_values_match_products_keys(self, lowercase_key: str, original_key: str) -> None:
        assert original_key in Products
        assert lowercase_key == original_key.lower()

    @pytest.mark.parametrize("key, expected_value", [
        ("outlaw", "Outlaw"),
        ("chieftain", "Chieftain"),
        ("king jester", "King Jester"),
        ("flame bt", "Flame BT"),
        ("mg bt", "MG BT"),
        ("stain spg", "Stain SPG"),
        ("rsc", "RSC")
    ])
    def test_lowercase_lookup_for_vehicles(self, key: str, expected_value: str) -> None:
        assert lowercase_product_map[key] == expected_value


# Test list_of_products
class TestListOfProducts:
    def test_list_matches_products_keys(self) -> None:
        assert set(list_of_products) == set(Products.keys())

    def test_list_length_matches_products(self) -> None:
        assert len(list_of_products) == len(Products)


# Test main_loop function
class TestMainLoop:
    @pytest.mark.parametrize("test_id, user_inputs, expected_outputs", [
        (
            "single_product_no_materials",
            ["0", "Outlaw", "2", "done"],
            ["You chose: 2 Outlaw", "Total resources needed", "N/A"]
        ),
        (
            "single_product_with_materials",
            ["1", "Chieftain", "1", "done"],
            ["You chose: 1 Chieftain", "Total Facility Materials needed"]
        ),
        (
            "case_insensitive_selection",
            ["0", "outlaw", "3", "done"],
            ["You chose: 3 Outlaw"]
        ),
        (
            "multiple_products",
            ["0", "Outlaw", "2", "Chieftain", "3", "done"],
            ["You chose: 2 Outlaw", "You chose: 3 Chieftain", "Calculating resources needed for [('Outlaw', 2), ('Chieftain', 3)]"]
        ),
        (
            "accumulate_same_product",
            ["0", "Outlaw", "2", "Outlaw", "3", "done"],
            ["You chose: 2 Outlaw", "You chose: 3 Outlaw", "Calculating resources needed for [('Outlaw', 2), ('Outlaw', 3)]"]
        ),
        (
            "invalid_product_then_valid",
            ["0", "Silverhand", "Outlaw", "1", "done"],
            ["Invalid choice", "You chose: 1 Outlaw"]
        ),
        (
            "immediate_exit",
            ["0", "done"],
            ["Calculating resources needed"]
        ),
    ])
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_loop_scenarios(
        self, 
        mock_print: MagicMock, 
        mock_input: MagicMock, 
        test_id: str, 
        user_inputs: list[str], 
        expected_outputs: list[str]
    ) -> None:
        from main import main_loop

        # Setup inputs
        mock_input.side_effect = user_inputs

        # Execute
        main_loop()

        # Verify outputs
        print_calls = [str(call) for call in mock_print.call_args_list]
        for expected in expected_outputs:
            assert any(expected in call for call in print_calls), f"Test '{test_id}' failed: Expected '{expected}' in output"
        
        # We can't easily verify the internal accumulation in users_map_of_products
        # because we patched it with a new dict, but we can verify the behavior via print output
        # or by checking if calculate_total_resources was called with the summed dictionary if we mocked it.
        # But here we are just checking the main_loop logic.

