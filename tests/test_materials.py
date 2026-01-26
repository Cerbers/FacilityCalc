import pytest
from materials import Material, Coke, Cmat, PCmat, Steel, A1

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

def test_steel_basic_resources() -> None:
    """Test resource calculation for Steel."""
    resources = Steel.total_basic_resources()
    assert resources["Salvage"] == 300.0
    assert resources["Sulfur"] == 60.0
    assert resources["Coal"] == pytest.approx(151.25)

def test_a1_basic_resources() -> None:
    """Test resource calculation for A1."""
    resources = A1.total_basic_resources()
    assert resources["Salvage"] == 15.0
    assert resources["Coal"] == pytest.approx(90.75)
