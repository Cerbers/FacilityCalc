"""
 GUI tests for callback-level happy paths.
"""
import builtins
from collections.abc import Iterator
from unittest.mock import call, patch

import pytest

import gui


@pytest.fixture(autouse=True)
def reset_gui_state() -> Iterator[None]:
    original_selected_products = list(gui.selected_products)
    original_recipe_combo_tags = dict(gui.recipe_combo_tags)
    original_output_font = gui._output_font
    original_output_font_bold = gui._output_font_bold

    gui.selected_products.clear()
    gui.recipe_combo_tags.clear()
    gui._output_font = None
    gui._output_font_bold = None

    yield

    gui.selected_products.clear()
    gui.selected_products.extend(original_selected_products)
    gui.recipe_combo_tags.clear()
    gui.recipe_combo_tags.update(original_recipe_combo_tags)
    gui._output_font = original_output_font
    gui._output_font_bold = original_output_font_bold


def test_add_product_callback_adds_valid_selection() -> None:
    values = {"product_combo": "Outlaw", "qty_input": 2}

    with patch("gui.dpg.get_value", side_effect=lambda tag: values[tag]):
        with patch("gui.refresh_selection_list") as mock_refresh_selection_list:
            gui.add_product_callback()

    assert gui.selected_products == [("Outlaw", 2)]
    mock_refresh_selection_list.assert_called_once_with()


def test_refresh_selection_list_renders_selected_products() -> None:
    gui.selected_products.extend([("Outlaw", 2), ("Chieftain", 1)])

    with patch("gui.dpg.delete_item") as mock_delete_item:
        with patch("gui.dpg.add_text") as mock_add_text:
            gui.refresh_selection_list()

    mock_delete_item.assert_called_once_with("selection_list_panel", children_only=True)
    mock_add_text.assert_has_calls(
        [
            call("  2x  Outlaw", parent="selection_list_panel"),
            call("  1x  Chieftain", parent="selection_list_panel"),
        ]
    )


def test_clear_list_callback_clears_selected_products() -> None:
    gui.selected_products.extend([("Outlaw", 2), ("Chieftain", 1)])

    with patch("gui.refresh_selection_list") as mock_refresh_selection_list:
        gui.clear_list_callback()

    assert gui.selected_products == []
    mock_refresh_selection_list.assert_called_once_with()


def test_emit_lines_formats_product_lines() -> None:
    captured = "Outlaw x2: {'Salvage': 500}\nSummary line"

    with patch("gui._append_product_line") as mock_append_product_line:
        with patch("gui.append_output") as mock_append_output:
            gui._emit_lines(captured)

    mock_append_product_line.assert_called_once_with("Outlaw", 2, "{'Salvage': 500}")
    mock_append_output.assert_called_once_with("Summary line")


def test_run_calculation_callback_emits_happy_path_output() -> None:
    gui.selected_products.extend([("Outlaw", 2)])

    def fake_calculate_total_resources(
        user_selections: list[tuple[str, int]],
        products: dict[str, object],
    ) -> dict[str, float]:
        assert user_selections == [("Outlaw", 2)]
        assert "Outlaw" in products
        builtins.print("Outlaw x2: {'Salvage': 500, 'Coal': 10}")
        return {"Salvage": 500.0, "Coal": 10.0}

    def fake_get_materials(
        user_selections: list[tuple[str, int]],
        products: dict[str, object],
    ) -> dict[str, float]:
        assert user_selections == [("Outlaw", 2)]
        assert "Outlaw" in products
        builtins.print("Outlaw x2: {'Cmat': 30}")
        return {"Cmat": 30.0}

    with patch("gui.calculate_total_resources", side_effect=fake_calculate_total_resources):
        with patch("gui.get_materials", side_effect=fake_get_materials):
            with patch("gui.append_output") as mock_append_output:
                with patch("gui._emit_lines") as mock_emit_lines:
                    with patch("gui._append_total_line") as mock_append_total_line:
                        gui.run_calculation_callback()

    assert mock_append_output.call_args_list == [
        call("------------------------------------------------------------"),
        call("Running: [('Outlaw', 2)]"),
        call(""),
        call(""),
        call("--- Facility Materials breakdown ---"),
        call(""),
    ]
    assert mock_emit_lines.call_args_list == [
        call("Outlaw x2: {'Salvage': 500, 'Coal': 10}\n"),
        call("Outlaw x2: {'Cmat': 30}\n"),
    ]
    assert mock_append_total_line.call_args_list == [
        call("Total basic resources", "{'Salvage': 500, 'Coal': 10}"),
        call("Total facility materials", "{'Cmat': 30}"),
    ]


def test_save_recipes_callback_updates_changed_recipe() -> None:
    class DummyMaterial:
        recipes = {
            "Old Recipe": {"Coal": 1.0},
            "New Recipe": {"Coal": 2.0},
        }
        cost = recipes["Old Recipe"]
        current_recipe = "Old Recipe"

        @classmethod
        def set_recipe(cls, recipe_name: str) -> None:
            if recipe_name not in cls.recipes:
                raise ValueError(f"Unknown recipe '{recipe_name}' for {cls.__name__}")
            cls.cost = cls.recipes[recipe_name]
            cls.current_recipe = recipe_name

    gui.recipe_combo_tags["Coke"] = "recipe_combo_Coke"

    with patch("gui.get_switchable_materials", return_value={"Coke": DummyMaterial}):
        with patch("gui.dpg.does_item_exist", return_value=True):
            with patch("gui.dpg.get_value", return_value="New Recipe"):
                with patch("gui.append_output") as mock_append_output:
                    gui.save_recipes_callback()

    assert DummyMaterial.current_recipe == "New Recipe"
    assert mock_append_output.call_args_list == [
        call("Recipes updated:"),
        call("  Coke: New Recipe"),
    ]
