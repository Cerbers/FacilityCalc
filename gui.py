import io
import contextlib
import dearpygui.dearpygui as dpg

from main import Products, list_of_products
from functions import calculate_total_resources, get_materials
from materials import get_switchable_materials, load_recipe_preferences

# --- State ---
selected_products: list[tuple[str, int]] = []
recipe_combo_tags: dict[str, str] = {}


# --- Helpers ---

def append_output(text: str) -> None:
    dpg.add_text(text, parent="output_panel")
    dpg.set_y_scroll("output_panel", dpg.get_y_scroll_max("output_panel"))


def refresh_selection_list() -> None:
    dpg.delete_item("selection_list_panel", children_only=True)
    if not selected_products:
        dpg.add_text("(empty)", parent="selection_list_panel", color=(120, 120, 120, 255))
    for name, qty in selected_products:
        dpg.add_text(f"  {qty}x  {name}", parent="selection_list_panel")


# --- Callbacks ---

def add_product_callback() -> None:
    product = dpg.get_value("product_combo")
    qty = dpg.get_value("qty_input")
    if not product:
        append_output("[!] No product selected.")
        return
    if product not in Products:
        append_output(f"[!] '{product}' not found in product list.")
        return
    selected_products.append((product, qty))
    refresh_selection_list()


def run_calculation_callback() -> None:
    if not selected_products:
        append_output("[!] No products in the list. Add at least one product first.")
        return

    append_output("─" * 60)
    append_output(f"Running: {[(name, qty) for name, qty in selected_products]}")
    append_output("")

    # Capture per-product breakdown printed by calculate_total_resources
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        total = calculate_total_resources(selected_products, Products)
    for line in buf.getvalue().splitlines():
        append_output(line)

    append_output(f"Total basic resources:  { {k: int(v) for k, v in total.items()} }")

    # Capture per-product materials printed by get_materials
    buf2 = io.StringIO()
    with contextlib.redirect_stdout(buf2):
        total_mats = get_materials(selected_products, Products)
    append_output("")
    append_output("--- Facility Materials breakdown ---")
    for line in buf2.getvalue().splitlines():
        append_output(line)
    append_output(f"Total facility materials: { {k: int(v) for k, v in total_mats.items()} }")
    append_output("")


def clear_list_callback() -> None:
    selected_products.clear()
    refresh_selection_list()


def save_recipes_callback() -> None:
    switchable = get_switchable_materials()
    changed: list[str] = []
    for mat_key, mat_class in switchable.items():
        tag = recipe_combo_tags.get(mat_key)
        if not tag or not dpg.does_item_exist(tag):
            continue
        chosen = dpg.get_value(tag)
        if chosen and chosen != mat_class.current_recipe:
            try:
                mat_class.set_recipe(chosen)
                changed.append(f"  {mat_key}: {chosen}")
            except ValueError as e:
                append_output(f"[!] {e}")
    if changed:
        append_output("Recipes updated:")
        for line in changed:
            append_output(line)
    else:
        append_output("Recipes: no changes.")


# --- Theme ---

def build_theme() -> int:
    with dpg.theme() as theme_id:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg,       (0,   0,   0,   255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg,        (45,  45,  45,  255))
            dpg.add_theme_color(dpg.mvThemeCol_PopupBg,        (35,  35,  35,  255))
            dpg.add_theme_color(dpg.mvThemeCol_Tab,            (55,  55,  55,  255))
            dpg.add_theme_color(dpg.mvThemeCol_TabActive,      (80,  80,  80,  255))
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered,     (70,  70,  70,  255))
            dpg.add_theme_color(dpg.mvThemeCol_Text,           (210, 210, 210, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button,         (70,  110, 160, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,  (90,  130, 180, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,   (55,  90,  140, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg,        (30,  30,  30,  255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (50,  50,  50,  255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg,        (20,  20,  20,  255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive,  (30,  30,  30,  255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg,    (20,  20,  20,  255))
            dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab,  (65,  65,  65,  255))
            dpg.add_theme_color(dpg.mvThemeCol_Separator,      (80,  80,  80,  255))
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding,  10, 10)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing,    8,  5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding,   6,  4)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding,    4)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding,  4)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding,   4)
    return theme_id  # type: ignore[return-value]


# --- Main ---

def main() -> None:
    load_recipe_preferences()

    dpg.create_context()
    theme_id = build_theme()

    with dpg.window(tag="primary_window"):
        with dpg.group(horizontal=True):

            # ── LEFT PANEL ────────────────────────────────────────────
            with dpg.child_window(width=430, height=-1, tag="left_panel", border=False):
                with dpg.tab_bar():

                    # ── Products tab ──────────────────────────────────
                    with dpg.tab(label="Products"):
                        dpg.add_spacer(height=4)
                        dpg.add_text("Product:")
                        dpg.add_combo(
                            items=list_of_products,
                            tag="product_combo",
                            width=400,
                            default_value=list_of_products[0] if list_of_products else "",
                        )
                        dpg.add_spacer(height=6)
                        dpg.add_text("Quantity:")
                        dpg.add_input_int(
                            tag="qty_input",
                            default_value=1,
                            min_value=1,
                            min_clamped=True,
                            width=120,
                        )
                        dpg.add_spacer(height=8)
                        dpg.add_button(
                            label="  Add to List  ",
                            callback=add_product_callback,
                            width=150,
                        )
                        dpg.add_spacer(height=10)
                        dpg.add_separator()
                        dpg.add_spacer(height=6)
                        dpg.add_text("Selected products:")
                        with dpg.child_window(
                            height=200,
                            tag="selection_list_panel",
                            border=True,
                        ):
                            dpg.add_text(
                                "(empty)",
                                color=(120, 120, 120, 255),
                            )
                        dpg.add_spacer(height=10)
                        with dpg.group(horizontal=True):
                            dpg.add_button(
                                label="  Run Calculation  ",
                                callback=run_calculation_callback,
                                width=170,
                            )
                            dpg.add_spacer(width=8)
                            dpg.add_button(
                                label="  Clear List  ",
                                callback=clear_list_callback,
                                width=120,
                            )

                    # ── Recipes tab ───────────────────────────────────
                    with dpg.tab(label="Recipes"):
                        dpg.add_spacer(height=4)
                        dpg.add_text(
                            "Select refinement recipe for each material, then save.",
                            color=(170, 170, 170, 255),
                        )
                        dpg.add_spacer(height=10)

                        switchable = get_switchable_materials()
                        for mat_key, mat_class in switchable.items():
                            recipe_names = list(mat_class.recipes.keys())
                            tag = f"recipe_combo_{mat_key}"
                            recipe_combo_tags[mat_key] = tag

                            dpg.add_text(f"{mat_key}:")
                            dpg.add_combo(
                                items=recipe_names,
                                default_value=mat_class.current_recipe,
                                tag=tag,
                                width=400,
                            )
                            dpg.add_spacer(height=6)

                        dpg.add_spacer(height=4)
                        dpg.add_separator()
                        dpg.add_spacer(height=8)
                        dpg.add_button(
                            label="  Save Recipe Changes  ",
                            callback=save_recipes_callback,
                            width=200,
                        )

            # ── RIGHT PANEL (output terminal) ─────────────────────────
            with dpg.child_window(width=-1, height=-1, tag="output_panel", border=True):
                dpg.add_text(
                    "Output will appear here after you run a calculation.",
                    color=(120, 120, 120, 255),
                )

    dpg.bind_theme(theme_id)
    dpg.create_viewport(title="FacilityCalc", width=1100, height=680)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("primary_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
