import pytest
from unittest.mock import patch, MagicMock
from typing import Type

from products import (
    Outlaw, Chieftain, Thornfall, Blinder, Skycaller, RAC, King_Jester,
    Flame_BT, MG_BT, SPG, StormCannon, IntelCenter, UndergroundFortress,
    RSC, Warden_Submarine, Frigate, Bluefin, Longhook, Bowhead, Prod, Firebrand
)
from main import Products, lowercase_product_map, list_of_products


# Test Products dictionary
class TestProductsDictionary:
    def test_products_contains_all_vehicles(self) -> None:
        expected_keys = [
            "Outlaw", "Chieftain", "Thornfall", "Blinder", "Skycaller", "RAC",
            "King_Jester", "Flame_BT", "MG_BT", "SPG", "StormCannon", "IntelCenter", "UndergroundFortress",
            "RSC", "Warden_Submarine", "Frigate", "Bluefin", "Longhook", "Bowhead", "Firebrand"
        ]
        for key in expected_keys:
            assert key in Products, f"Missing product: {key}"

    def test_products_maps_to_correct_classes(self) -> None:
        assert Products["Outlaw"] is Outlaw
        assert Products["Chieftain"] is Chieftain
        assert Products["Thornfall"] is Thornfall
        assert Products["Blinder"] is Blinder
        assert Products["Skycaller"] is Skycaller
        assert Products["RAC"] is RAC
        assert Products["King_Jester"] is King_Jester
        assert Products["Flame_BT"] is Flame_BT
        assert Products["MG_BT"] is MG_BT
        assert Products["SPG"] is SPG
        assert Products["StormCannon"] is StormCannon
        assert Products["IntelCenter"] is IntelCenter
        assert Products["UndergroundFortress"] is UndergroundFortress
        assert Products["RSC"] is RSC
        assert Products["Warden_Submarine"] is Warden_Submarine
        assert Products["Frigate"] is Frigate
        assert Products["Bluefin"] is Bluefin
        assert Products["Longhook"] is Longhook
        assert Products["Bowhead"] is Bowhead
        assert Products["Firebrand"] is Firebrand

    def test_all_products_are_prod_subclasses(self) -> None:
        for name, product_class in Products.items():
            assert issubclass(product_class, Prod), f"{name} is not a Prod subclass"


# Test lowercase_product_map
class TestLowercaseProductMap:
    def test_lowercase_map_has_same_length_as_products(self) -> None:
        assert len(lowercase_product_map) == len(Products)

    def test_lowercase_map_keys_are_lowercase(self) -> None:
        for key in lowercase_product_map.keys():
            assert key == key.lower(), f"Key '{key}' is not lowercase"

    def test_lowercase_map_values_match_products_keys(self) -> None:
        for lowercase_key, original_key in lowercase_product_map.items():
            assert original_key in Products
            assert lowercase_key == original_key.lower()

    def test_lowercase_lookup_for_vehicles(self) -> None:
        assert lowercase_product_map["outlaw"] == "Outlaw"
        assert lowercase_product_map["chieftain"] == "Chieftain"
        assert lowercase_product_map["king_jester"] == "King_Jester"
        assert lowercase_product_map["flame_bt"] == "Flame_BT"
        assert lowercase_product_map["rsc"] == "RSC"


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

