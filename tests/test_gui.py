"""
GUI Phase 1 tests — business-logic layer used by the GUI.

These mirror the scenarios in test_main.py::TestMainLoop but call
calculate_total_resources / get_materials directly instead of mocking stdin/stdout,
because the GUI drives those functions without a CLI loop.
"""
import pytest
from unittest.mock import patch, MagicMock
from typing import Type

from products import Prod, name_mappings
from main import Products, list_of_products
from functions import calculate_total_resources, get_materials


# ---------------------------------------------------------------------------
# Product / alias resolution (the GUI uses name_mappings for text input
# fallback; for dropdowns it uses list_of_products directly)
# ---------------------------------------------------------------------------

class TestGuiProductSelection:
    def test_canonical_names_present(self) -> None:
        assert "Outlaw" in Products
        assert "Chieftain" in Products

    def test_case_insensitive_lookup(self) -> None:
        assert name_mappings.get("outlaw") == "Outlaw"
        assert name_mappings.get("chieftain") == "Chieftain"

    def test_alias_atht_resolves_to_blinder(self) -> None:
        assert name_mappings.get("atht") == "Blinder"

    def test_alias_rocket_ac_resolves_to_rac(self) -> None:
        assert name_mappings.get("rocket ac") == "RAC"

    def test_list_of_products_matches_products_keys(self) -> None:
        assert set(list_of_products) == set(Products.keys())


# ---------------------------------------------------------------------------
# Calculation correctness (mirrors TestMainLoop scenarios)
# ---------------------------------------------------------------------------

class TestGuiCalculation:
    """
    Each test patches builtins.print so calculate_total_resources / get_materials
    don't pollute test output, then checks the return values and captured calls.
    """

    @patch("builtins.print")
    def test_single_product_no_materials_flag(self, mock_print: MagicMock) -> None:
        """Mirrors: single_product_no_materials — Outlaw x2, no materials toggle."""
        selections = [("Outlaw", 2)]
        result = calculate_total_resources(selections, Products)
        assert isinstance(result, dict)
        assert len(result) > 0
        calls = [str(c) for c in mock_print.call_args_list]
        assert any("Outlaw" in c for c in calls)

    @patch("builtins.print")
    def test_single_product_with_materials(self, mock_print: MagicMock) -> None:
        """Mirrors: single_product_with_materials — Chieftain x1."""
        selections = [("Chieftain", 1)]
        basic = calculate_total_resources(selections, Products)
        mats = get_materials(selections, Products)
        assert isinstance(basic, dict) and len(basic) > 0
        assert isinstance(mats, dict) and len(mats) > 0

    @patch("builtins.print")
    def test_case_insensitive_selection(self, mock_print: MagicMock) -> None:
        """Mirrors: case_insensitive_selection — resolve 'outlaw' then calc x3."""
        canonical = name_mappings.get("outlaw")
        assert canonical == "Outlaw"
        result = calculate_total_resources([(canonical, 3)], Products)
        assert len(result) > 0
        calls = [str(c) for c in mock_print.call_args_list]
        assert any("Outlaw" in c for c in calls)

    @patch("builtins.print")
    def test_multiple_products(self, mock_print: MagicMock) -> None:
        """Mirrors: multiple_products — Outlaw x2 + Chieftain x3."""
        selections = [("Outlaw", 2), ("Chieftain", 3)]
        result = calculate_total_resources(selections, Products)
        assert len(result) > 0
        calls = [str(c) for c in mock_print.call_args_list]
        assert any("Outlaw" in c for c in calls)
        assert any("Chieftain" in c for c in calls)

    @patch("builtins.print")
    def test_accumulate_same_product(self, mock_print: MagicMock) -> None:
        """Mirrors: accumulate_same_product — Outlaw x2 then Outlaw x3."""
        selections = [("Outlaw", 2), ("Outlaw", 3)]
        result = calculate_total_resources(selections, Products)
        assert len(result) > 0
        calls = [str(c) for c in mock_print.call_args_list]
        assert sum(1 for c in calls if "Outlaw" in c) == 2

    @patch("builtins.print")
    def test_alias_selection_atht(self, mock_print: MagicMock) -> None:
        """Mirrors: alias_selection — 'atht' → Blinder x1."""
        canonical = name_mappings.get("atht")
        assert canonical == "Blinder"
        assert canonical in Products
        result = calculate_total_resources([(canonical, 1)], Products)
        assert len(result) > 0
        calls = [str(c) for c in mock_print.call_args_list]
        assert any("Blinder" in c for c in calls)

    @patch("builtins.print")
    def test_alias_selection_rac(self, mock_print: MagicMock) -> None:
        """Mirrors: alias_selection_rac — 'rocket ac' → RAC x1."""
        canonical = name_mappings.get("rocket ac")
        assert canonical == "RAC"
        assert canonical in Products
        result = calculate_total_resources([(canonical, 1)], Products)
        assert len(result) > 0

    @patch("builtins.print")
    def test_resources_scale_with_quantity(self, mock_print: MagicMock) -> None:
        """Basic sanity: doubling quantity doubles every resource value."""
        r1 = calculate_total_resources([("Outlaw", 1)], Products)
        r2 = calculate_total_resources([("Outlaw", 2)], Products)
        for key in r1:
            assert pytest.approx(r2[key]) == r1[key] * 2

    @patch("builtins.print")
    def test_get_materials_returns_dict(self, mock_print: MagicMock) -> None:
        """get_materials must return a non-empty dict for any valid product."""
        result = get_materials([("Chieftain", 1)], Products)
        assert isinstance(result, dict)
        assert len(result) > 0
