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
            "Outlaw", "Chieftain", "Thornfall", "ATHT", "Skycaller", "RAC",
            "King Jester", "Flame BT", "MG BT", "SPG", "SC", "IC", "UF",
            "RSC", "Nakki", "Frigate", "Bluefin", "Longhook", "Bowhead", "Firebrand"
        ]
        for key in expected_keys:
            assert key in Products, f"Missing product: {key}"

    def test_products_maps_to_correct_classes(self) -> None:
        assert Products["Outlaw"] is Outlaw
        assert Products["Chieftain"] is Chieftain
        assert Products["Thornfall"] is Thornfall
        assert Products["ATHT"] is Blinder
        assert Products["Skycaller"] is Skycaller
        assert Products["RAC"] is RAC
        assert Products["King Jester"] is King_Jester
        assert Products["Flame BT"] is Flame_BT
        assert Products["MG BT"] is MG_BT
        assert Products["SPG"] is SPG
        assert Products["SC"] is StormCannon
        assert Products["IC"] is IntelCenter
        assert Products["UF"] is UndergroundFortress
        assert Products["RSC"] is RSC
        assert Products["Nakki"] is Warden_Submarine
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
        assert lowercase_product_map["king jester"] == "King Jester"
        assert lowercase_product_map["flame bt"] == "Flame BT"
        assert lowercase_product_map["rsc"] == "RSC"


# Test list_of_products
class TestListOfProducts:
    def test_list_matches_products_keys(self) -> None:
        assert set(list_of_products) == set(Products.keys())

    def test_list_length_matches_products(self) -> None:
        assert len(list_of_products) == len(Products)


# Test main_loop function
class TestMainLoop:
    @patch('main.users_map_of_products', {})
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_loop_single_product_no_materials(
        self, mock_print: MagicMock, mock_input: MagicMock
    ) -> None:
        from main import main_loop

        # User selects "no materials", picks Outlaw, quantity 2, then exits
        mock_input.side_effect = ["0", "Outlaw", "2", "done"]

        main_loop()

        # Verify print was called with results
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Total resources needed" in call for call in print_calls)
        assert any("N/A" in call for call in print_calls)

    @patch('main.users_map_of_products', {})
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_loop_with_materials_display(
        self, mock_print: MagicMock, mock_input: MagicMock
    ) -> None:
        from main import main_loop

        # User selects "show materials", picks Chieftain, quantity 1, then exits
        mock_input.side_effect = ["1", "Chieftain", "1", "done"]

        main_loop()

        # Verify print was called with material results (not N/A)
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Total Facility Materials needed" in call for call in print_calls)

    @patch('main.users_map_of_products', {})
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_loop_invalid_product_then_valid(
        self, mock_print: MagicMock, mock_input: MagicMock
    ) -> None:
        from main import main_loop

        # User enters invalid product, then valid one
        mock_input.side_effect = ["0", "Silverhand", "Outlaw", "1", "done"]

        main_loop()

        # Verify invalid choice message was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Invalid choice" in call for call in print_calls)

    @patch('main.users_map_of_products', {})
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_loop_case_insensitive_product_selection(
        self, mock_print: MagicMock, mock_input: MagicMock
    ) -> None:
        from main import main_loop

        # User enters lowercase product name
        mock_input.side_effect = ["0", "outlaw", "3", "done"]

        main_loop()

        # Verify the product was accepted
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("You chose: 3 Outlaw" in call for call in print_calls)

    @patch('main.users_map_of_products', {})
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_loop_multiple_products(
        self, mock_print: MagicMock, mock_input: MagicMock
    ) -> None:
        from main import main_loop

        # User selects multiple products
        mock_input.side_effect = ["0", "Outlaw", "2", "Chieftain", "3", "done"]

        main_loop()

        # Verify both products were acknowledged
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("You chose: 2 Outlaw" in call for call in print_calls)
        assert any("You chose: 3 Chieftain" in call for call in print_calls)

    @patch('main.users_map_of_products', {})
    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_loop_immediate_exit(
        self, mock_print: MagicMock, mock_input: MagicMock
    ) -> None:
        from main import main_loop

        # User immediately exits without selecting products
        mock_input.side_effect = ["0", "done"]

        main_loop()

        # Verify calculation was still attempted (with empty selection)
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert any("Calculating resources needed" in call for call in print_calls)
