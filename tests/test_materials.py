import pytest
import json
from unittest.mock import patch, mock_open
from materials import (
    Material, Coke, Cmat, PCmat, Steel, A1, A3, A4, EnrichedOil,
    AircraftMechanicalPartsSmall, AircraftMechanicalPartsLarge,
    AircraftEngineSmall, AircraftEngineLarge,
    get_switchable_materials, load_recipe_preferences
)


@pytest.fixture(autouse=True)
def reset_recipes():
    """Reset all material recipes to defaults before and after each test."""
    Coke.set_recipe("Coke Furnace")
    Cmat.set_recipe("Metal Press")
    PCmat.set_recipe("Recycler")
    Steel.set_recipe("Default")
    EnrichedOil.set_recipe("Oil Refinery")
    yield
    Coke.set_recipe("Coke Furnace")
    Cmat.set_recipe("Metal Press")
    PCmat.set_recipe("Recycler")
    Steel.set_recipe("Default")
    EnrichedOil.set_recipe("Oil Refinery")



def test_material_empty_cost_exception() -> None:
    """Test that calculating resources for a Material with empty cost raises ValueError."""
    class EmptyMaterial(Material):
        cost = {}

    with pytest.raises(ValueError, match="No attributes in cost dictionary in EmptyMaterial"):
        EmptyMaterial.total_basic_resources()

def test_coke_basic_resources() -> None:
    """Test resource calculation for Coke."""
    resources = Coke.total_basic_resources()
    assert resources == {"Coal": 1.21}

def test_cmat_basic_resources() -> None:
    """Test resource calculation for Cmat."""
    resources = Cmat.total_basic_resources()
    assert resources == {"Salvage": 5.0}

def test_pcmat_basic_resources() -> None:
    """Test resource calculation for PCmat."""
    resources = PCmat.total_basic_resources()
    assert resources == {"Salvage": 100.0}

@pytest.mark.parametrize("resource, expected_amount", [
    ("Salvage", 300.0),
    ("Sulfur", 60.0),
    ("Coal", 151.25)
])
def test_steel_basic_resources(resource: str, expected_amount: float) -> None:
    """Test resource calculation for Steel."""
    resources = Steel.total_basic_resources()
    assert resources[resource] == pytest.approx(expected_amount)

@pytest.mark.parametrize("resource, expected_amount", [
    ("Salvage", 15.0),
    ("Coal", 90.75)
])
def test_a1_basic_resources(resource: str, expected_amount: float) -> None:
    """Test resource calculation for A1."""
    resources = A1.total_basic_resources()
    assert resources[resource] == pytest.approx(expected_amount)


# === Recipe system tests ===

def test_set_recipe_changes_cost() -> None:
    """Test that set_recipe swaps the cost dict."""
    Coke.set_recipe("Coal Refinery Basic")
    assert Coke.cost == {"Coal": 1.11}

def test_set_recipe_invalid_name() -> None:
    """Test that set_recipe raises ValueError for unknown recipe."""
    with pytest.raises(ValueError, match="Unknown recipe"):
        Coke.set_recipe("Nonexistent Recipe")

def test_set_recipe_updates_current_recipe() -> None:
    """Test that current_recipe tracks the active recipe name."""
    Coke.set_recipe("Coal Refinery Basic")
    assert Coke.current_recipe == "Coal Refinery Basic"

def test_set_recipe_on_material_without_recipes() -> None:
    """Test that set_recipe raises ValueError on materials without recipes."""
    with pytest.raises(ValueError, match="Unknown recipe"):
        A1.set_recipe("anything")

def test_material_without_recipes_has_empty_recipes() -> None:
    """Test that materials without alt recipes have empty recipes dict."""
    assert A1.recipes == {}


# === get_switchable_materials tests ===

def test_get_switchable_materials_includes_recipe_materials() -> None:
    """Test that switchable materials includes all materials with recipes."""
    switchable = get_switchable_materials()
    assert "Coke" in switchable
    assert "Cmat" in switchable
    assert "PCmat" in switchable
    assert "Steel" in switchable
    assert "EnrichedOil" in switchable

def test_get_switchable_materials_excludes_simple_materials() -> None:
    """Test that switchable materials excludes materials without recipes."""
    switchable = get_switchable_materials()
    assert "A1" not in switchable
    assert "A2" not in switchable
    assert "A4" not in switchable


# === Recipe-specific resolution tests ===

def test_coke_coal_refinery_recipe() -> None:
    """Test Coke with Coal Refinery Basic recipe."""
    Coke.set_recipe("Coal Refinery Basic")
    resources = Coke.total_basic_resources()
    assert resources == {"Coal": 1.11}

def test_cmat_smelter_recipe_includes_coal() -> None:
    """Test Cmat Smelter recipe resolves Coke to Coal."""
    Cmat.set_recipe("Smelter")
    resources = Cmat.total_basic_resources()

    assert resources["Salvage"] == pytest.approx(5.0)
    assert resources["Coal"] == pytest.approx(8.333 * 1.21)

def test_cmat_material_factory_recipe() -> None:
    """Test Cmat Material Factory recipe."""
    Cmat.set_recipe("Material Factory")
    resources = Cmat.total_basic_resources()
    assert resources == {"Salvage": 10.0}

def test_pcmat_metalworks_recipe_has_components() -> None:
    """Test PCmat Metalworks recipe resolves Components as basic resource."""
    PCmat.set_recipe("Metalworks")
    resources = PCmat.total_basic_resources()

    assert resources["Components"] == pytest.approx(20.0)
    assert resources["Salvage"] == pytest.approx(15.0)

def test_enriched_oil_default_recipe() -> None:
    """Test EnrichedOil default recipe (Oil Refinery)."""
    resources = EnrichedOil.total_basic_resources()
    assert resources == {"Sulfur": 60.0}

def test_enriched_oil_offshore_recipe() -> None:
    """Test EnrichedOil with Offshore Platform recipe."""
    EnrichedOil.set_recipe("Offshore Platform")
    resources = EnrichedOil.total_basic_resources()
    assert resources == {"Coal": 100.0}

def test_steel_enriched_oil_recipe_chain() -> None:
    """Test Steel with Enriched Oil recipe resolves through EnrichedOil material."""
    Steel.set_recipe("Enriched Oil")

    resources = Steel.total_basic_resources()
    assert "Sulfur" in resources  # from EnrichedOil
    assert "Salvage" in resources  # from PCmat
    assert "Coal" in resources  # from Coke
    assert resources["Sulfur"] == pytest.approx(60.0)  # 1 EnrichedOil * 60 Sulfur

def test_steel_enriched_oil_with_offshore_platform() -> None:
    """Test full chain: Steel (Enriched Oil) + EnrichedOil (Offshore Platform)."""
    Steel.set_recipe("Enriched Oil")
    EnrichedOil.set_recipe("Offshore Platform")

    resources = Steel.total_basic_resources()
    assert "Sulfur" not in resources  # no Sulfur source in this config
    assert resources["Coal"] == pytest.approx(125.0 * 1.21 + 100.0)  # Coke Coal + EnrichedOil Coal


def test_aircraft_mechanical_parts_small_cost() -> None:
    """Test AircraftMechanicalPartsSmall basic cost structure."""
    assert AircraftMechanicalPartsSmall.cost == {"PCmat": 35.0, "A3": 25.0}


def test_aircraft_engine_small_cost() -> None:
    """Test AircraftEngineSmall basic cost structure."""
    assert AircraftEngineSmall.cost == {"PCmat": 95.0, "A4": 25.0}


@pytest.mark.parametrize("resource, expected_amount", [
    ("Salvage", 3875.0),
    ("Sulfur", 500.0)
])
def test_aircraft_mechanical_parts_small_basic_resources(resource: str, expected_amount: float) -> None:
    """Test AircraftMechanicalPartsSmall resource resolution."""
    resources = AircraftMechanicalPartsSmall.total_basic_resources()
    assert resources[resource] == pytest.approx(expected_amount)


def test_aircraft_mechanical_parts_large_cost() -> None:
    """Test AircraftMechanicalPartsLarge basic cost structure."""
    assert AircraftMechanicalPartsLarge.cost == {"PCmat": 35.0, "A3": 25.0}


@pytest.mark.parametrize("resource, expected_amount", [
    ("Salvage", 3875.0),
    ("Sulfur", 500.0)
])
def test_aircraft_mechanical_parts_large_basic_resources(resource: str, expected_amount: float) -> None:
    """Test AircraftMechanicalPartsLarge resource resolution."""
    resources = AircraftMechanicalPartsLarge.total_basic_resources()
    assert resources[resource] == pytest.approx(expected_amount)


@pytest.mark.parametrize("resource, expected_amount", [
    ("Salvage", 12000.0),
])
def test_aircraft_engine_small_basic_resources(resource: str, expected_amount: float) -> None:
    """Test AircraftEngineSmall resource resolution."""
    resources = AircraftEngineSmall.total_basic_resources()
    assert resources[resource] == pytest.approx(expected_amount)


def test_aircraft_engine_large_cost() -> None:
    """Test AircraftEngineLarge basic cost structure."""
    assert AircraftEngineLarge.cost == {"PCmat": 95.0, "A4": 25.0}


@pytest.mark.parametrize("resource, expected_amount", [
    ("Salvage", 12000.0),
])
def test_aircraft_engine_large_basic_resources(resource: str, expected_amount: float) -> None:
    """Test AircraftEngineLarge resource resolution."""
    resources = AircraftEngineLarge.total_basic_resources()
    assert resources[resource] == pytest.approx(expected_amount)


# === Recipe preferences loading tests ===

def test_load_preferences_valid_file(capsys) -> None:
    """Test that valid preferences file loads recipes correctly."""
    prefs_json = '{"Coke": "Coal Refinery Basic", "Cmat": "Smelter"}'

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=prefs_json)):
            with patch("json.load", return_value={"Coke": "Coal Refinery Basic", "Cmat": "Smelter"}):
                load_recipe_preferences()

    assert Coke.cost == {"Coal": 1.11}
    assert Cmat.cost == {"Salvage": 5.0, "Coke": 8.333}


def test_load_preferences_invalid_recipe_name(capsys) -> None:
    """Test that invalid recipe name falls back to default with warning."""
    prefs_json = '{"Coke": "Nonexistent Recipe"}'

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=prefs_json)):
            with patch("json.load", return_value={"Coke": "Nonexistent Recipe"}):
                load_recipe_preferences()

    assert Coke.cost == {"Coal": 1.21}  # Default: Coke Furnace
    captured = capsys.readouterr()
    assert "Warning" in captured.out


def test_load_preferences_unknown_material(capsys) -> None:
    """Test that unknown material in preferences is skipped with warning."""
    prefs_json = '{"UnknownMaterial": "SomeRecipe", "Coke": "Coke Furnace"}'

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=prefs_json)):
            with patch("json.load", return_value={"UnknownMaterial": "SomeRecipe", "Coke": "Coke Furnace"}):
                load_recipe_preferences()

    assert Coke.cost == {"Coal": 1.21}  # Should still work
    captured = capsys.readouterr()
    assert "Unknown material" in captured.out


def test_load_preferences_missing_file(capsys) -> None:
    """Test that missing preferences file uses defaults without error."""
    with patch("os.path.exists", return_value=False):
        load_recipe_preferences()

    # Should remain at default
    assert Coke.cost == {"Coal": 1.21}


def test_load_preferences_malformed_json(capsys) -> None:
    """Test that malformed JSON uses defaults with warning."""
    malformed_json = "{ invalid json }"

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=malformed_json)):
            with patch("json.load", side_effect=json.JSONDecodeError("Expecting property name", "", 0)):
                load_recipe_preferences()

    assert Coke.cost == {"Coal": 1.21}  # Default
    captured = capsys.readouterr()
    assert "Warning" in captured.out


def test_load_preferences_empty_object(capsys) -> None:
    """Test that empty object {} uses all defaults."""
    prefs_json = "{}"

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=prefs_json)):
            with patch("json.load", return_value={}):
                load_recipe_preferences()

    # Should remain at defaults
    assert Coke.cost == {"Coal": 1.21}
    assert Cmat.cost == {"Salvage": 5.0}


def test_load_preferences_null_recipe_value(capsys) -> None:
    """Test that null recipe value is handled gracefully with warning."""
    prefs_json = '{"Coke": null}'

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=prefs_json)):
            with patch("json.load", return_value={"Coke": None}):
                load_recipe_preferences()

    assert Coke.cost == {"Coal": 1.21}  # Default
    captured = capsys.readouterr()
    assert "Warning" in captured.out


def test_load_preferences_non_string_recipe(capsys) -> None:
    """Test that non-string recipe value is handled gracefully with warning."""
    prefs_json = '{"Coke": 123}'

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=prefs_json)):
            with patch("json.load", return_value={"Coke": 123}):
                load_recipe_preferences()

    assert Coke.cost == {"Coal": 1.21}  # Default
    captured = capsys.readouterr()
    assert "Warning" in captured.out


def test_load_preferences_empty_file(capsys) -> None:
    """Test that empty file uses defaults with warning."""
    empty_json = ""

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=empty_json)):
            with patch("json.load", side_effect=json.JSONDecodeError("Expecting value", "", 0)):
                load_recipe_preferences()

    assert Coke.cost == {"Coal": 1.21}  # Default
    captured = capsys.readouterr()
    assert "Warning" in captured.out


def test_load_preferences_partially_valid_json(capsys) -> None:
    """Test that partially valid JSON applies valid entries and skips invalid ones."""
    prefs_json = '{"Coke": "Coal Refinery Basic", "UnknownMaterial": "SomeRecipe", "Cmat": "Smelter"}'

    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=prefs_json)):
            with patch("json.load", return_value={
                "Coke": "Coal Refinery Basic",
                "UnknownMaterial": "SomeRecipe",
                "Cmat": "Smelter"
            }):
                load_recipe_preferences()

    assert Coke.cost == {"Coal": 1.11}  # Applied valid preference
    assert Cmat.cost == {"Salvage": 5.0, "Coke": 8.333}  # Applied valid preference
    captured = capsys.readouterr()
    assert "Unknown material" in captured.out
