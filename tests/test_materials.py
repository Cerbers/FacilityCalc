import pytest
from materials import Material, Coke, Cmat, PCmat, Steel, A1, EnrichedOil, get_switchable_materials


@pytest.fixture(autouse=True)
def reset_recipes():
    """Reset all material recipes to defaults after each test."""
    yield
    Coke.set_recipe("Coke Furnace")
    Cmat.set_recipe("Metal Press (+Petrol)")
    PCmat.set_recipe("Recycler")
    Steel.set_recipe("Default")
    EnrichedOil.set_recipe("Oil Refinery (+Heavy Oil)")


# === Existing tests (defaults unchanged) ===

def test_material_empty_cost_exception() -> None:
    """Test that calculating resources for a Material with empty cost raises ValueError."""
    class EmptyMaterial(Material):
        cost = {}

    with pytest.raises(ValueError, match="No attributies in cost dictionary in EmptyMaterial"):
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
    # Smelter: 5 Salvage + 8.333 Coke
    # Coke default (Coke Furnace): 1.21 Coal per Coke
    # So: 5 Salvage + 8.333 * 1.21 Coal = 5 Salvage + 10.08293 Coal
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
    # Metalworks: 3 Cmat + 20 Components
    # Cmat default (Metal Press): 5 Salvage
    # So: 3 * 5 Salvage + 20 Components = 15 Salvage + 20 Components
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
    # Enriched Oil recipe: 3 PCmat + 125 Coke + 1 EnrichedOil
    # EnrichedOil default (Oil Refinery): 60 Sulfur
    # PCmat default (Recycler): 15 Cmat + 25 Salvage → 100 Salvage
    # Coke default (Coke Furnace): 1.21 Coal
    resources = Steel.total_basic_resources()
    assert "Sulfur" in resources  # from EnrichedOil
    assert "Salvage" in resources  # from PCmat
    assert "Coal" in resources  # from Coke
    assert resources["Sulfur"] == pytest.approx(60.0)  # 1 EnrichedOil * 60 Sulfur

def test_steel_enriched_oil_with_offshore_platform() -> None:
    """Test full chain: Steel (Enriched Oil) + EnrichedOil (Offshore Platform)."""
    Steel.set_recipe("Enriched Oil")
    EnrichedOil.set_recipe("Offshore Platform")
    # Steel: 3 PCmat + 125 Coke + 1 EnrichedOil
    # EnrichedOil (Offshore): 100 Coal
    # So EnrichedOil contributes Coal, not Sulfur
    resources = Steel.total_basic_resources()
    assert "Sulfur" not in resources  # no Sulfur source in this config
    assert resources["Coal"] == pytest.approx(125.0 * 1.21 + 100.0)  # Coke Coal + EnrichedOil Coal
