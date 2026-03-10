import pytest
from unittest.mock import patch, MagicMock
from typing import Type
import products
from products import Prod
from main import Products, name_mappings, list_of_products


class TestProducts:
    @pytest.mark.parametrize("name, product_class", Products.items())
    def test_product_is_prod_subclass(self, name: str, product_class: Type[Prod]) -> None:
        assert issubclass(product_class, Prod), f"{name} is not a Prod subclass"

    @pytest.mark.parametrize("name, product_class", Products.items())
    def test_product_has_valid_faction(self, name: str, product_class: Type[Prod]) -> None:
        assert hasattr(product_class, "faction"), f"{name} missing faction attribute"
        assert product_class.faction in ("warden", "colonial", "all"), f"{name} has invalid faction: {product_class.faction}"


class TestNameMappings:
    @pytest.mark.parametrize("key", name_mappings.keys())
    def test_all_mapping_keys_are_lowercase(self, key: str) -> None:
        assert key == key.lower(), f"Key '{key}' is not lowercase"

    @pytest.mark.parametrize("key, value", name_mappings.items())
    def test_all_mappings_point_to_valid_products(self, key: str, value: str) -> None:
        assert value in Products, f"Mapping '{key}' -> '{value}' points to non-existent product"

    @pytest.mark.parametrize("product_name, product_class", Products.items())
    def test_product_canonical_name_is_mapped(self, product_name: str, product_class: Type[Prod]) -> None:
        assert product_name.lower() in name_mappings, f"Canonical name '{product_name}' not in mappings"
        assert name_mappings[product_name.lower()] == product_name

    @pytest.mark.parametrize("product_name, product_class", Products.items())
    def test_product_all_names_are_mapped(self, product_name: str, product_class: Type[Prod]) -> None:
        for alias in product_class.names:
            alias_lower = alias.lower()
            assert alias_lower in name_mappings, f"Alias '{alias}' of '{product_name}' not in mappings"
            assert name_mappings[alias_lower] == product_name


class TestListOfProducts:
    def test_list_matches_products_keys(self) -> None:
        assert set(list_of_products) == set(Products.keys())

    def test_list_length_matches_products(self) -> None:
        assert len(list_of_products) == len(Products)


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
        (
            "alias_selection",
            ["0", "atht", "1", "done"],
            ["You chose: 1 Blinder"]
        ),
        (
            "alias_selection_rac",
            ["0", "rocket ac", "1", "done"],
            ["You chose: 1 RAC"]
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

        mock_input.side_effect = user_inputs

        main_loop()

        print_calls = [str(call) for call in mock_print.call_args_list]
        for expected in expected_outputs:
            assert any(expected in call for call in print_calls), f"Test '{test_id}' failed: Expected '{expected}' in output"


class TestMainLoopExit:
    @patch('builtins.input')
    @patch('builtins.print')
    def test_exit_at_vehicle_selection(self, mock_print: MagicMock, mock_input: MagicMock) -> None:
        """Typing 'exit' at the vehicle prompt returns without calculating."""
        from main import main_loop
        mock_input.side_effect = ["0", "exit"]
        main_loop()  # must return normally, not raise
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert not any("Calculating resources" in call for call in print_calls)

    @patch('builtins.input', side_effect=["0", "EXIT"])
    @patch('builtins.print')
    def test_exit_uppercase_at_vehicle_selection(self, mock_print: MagicMock, mock_input: MagicMock) -> None:
        """'EXIT' (uppercase) at the vehicle prompt also quits."""
        from main import main_loop
        main_loop()

    @patch('builtins.input', side_effect=["0", "Exit"])
    @patch('builtins.print')
    def test_exit_mixed_case_at_vehicle_selection(self, mock_print: MagicMock, mock_input: MagicMock) -> None:
        """'Exit' (mixed case) at the vehicle prompt also quits."""
        from main import main_loop
        main_loop()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_exit_at_quantity_prompt(self, mock_print: MagicMock, mock_input: MagicMock) -> None:
        """Typing 'exit' at the quantity prompt raises SystemExit."""
        from main import main_loop
        mock_input.side_effect = ["0", "Outlaw", "exit"]
        with pytest.raises(SystemExit):
            main_loop()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_exit_at_quantity_prompt_case_insensitive(self, mock_print: MagicMock, mock_input: MagicMock) -> None:
        """'EXIT' at quantity prompt also raises SystemExit."""
        from main import main_loop
        mock_input.side_effect = ["0", "Outlaw", "EXIT"]
        with pytest.raises(SystemExit):
            main_loop()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_exit_after_adding_products(self, mock_print: MagicMock, mock_input: MagicMock) -> None:
        """Exit at vehicle prompt after already selecting products - no calculation runs."""
        from main import main_loop
        mock_input.side_effect = ["0", "Outlaw", "2", "exit"]
        main_loop()
        print_calls = [str(call) for call in mock_print.call_args_list]
        assert not any("Calculating resources" in call for call in print_calls)
