import pytest
from products import (
    Prod, Chieftain, Thornfall, Outlaw, Blinder, RAC, Skycaller,
    King_Jester, MG_BT, Flame_BT, SPG, RSC, StormCannon,
    UndergroundFortress, IntelCenter, Frigate, Warden_Submarine, Bowhead,
    Longhook, Bluefin, Firebrand
)

def test_prod_empty_cost_exception() -> None:
    """Test that calculating resources for a Prod with empty cost raises ValueError."""
    class EmptyProduct(Prod):
        cost = {}
        
    with pytest.raises(ValueError, match="No attributies in cost dictionary in EmptyProduct"):
        EmptyProduct.total_basic_resources()

def test_prod_class_method() -> None:
    """Test the base Prod class functionality using a dummy subclass."""
    class TestProduct(Prod):
        cost = {
            "Cmat": 10.0,
            "A4": 2.0
        }
        
    resources = TestProduct.total_basic_resources()
    assert resources["Salvage"] == 250.0

def test_chieftain_resources() -> None:
    """Test resource calculation for Chieftain."""
    resources = Chieftain.total_basic_resources()
    assert resources["Salvage"] == 1450.0
    assert resources["Coal"] == pytest.approx(907.5)

def test_thornfall_resources() -> None:
    """Test resource calculation for Thornfall."""
    resources = Thornfall.total_basic_resources()
    assert resources["Salvage"] == 7875.0
    assert resources["Coal"] == pytest.approx(907.5)
    assert resources["Sulfur"] == 300.0

def test_outlaw_resources() -> None:
    """Test resource calculation for Outlaw."""
    resources = Outlaw.total_basic_resources()
    assert resources["Salvage"] == 2150.0
    assert resources["Coal"] == pytest.approx(907.5)

def test_blinder_resources() -> None:
    """Test resource calculation for Blinder."""
    resources = Blinder.total_basic_resources()
    assert resources["Salvage"] == 950.0

def test_rac_resources() -> None:
    """Test resource calculation for RAC."""
    resources = RAC.total_basic_resources()
    assert resources["Salvage"] == 3770.0
    assert resources["Coal"] == pytest.approx(907.5)
    assert resources["Sulfur"] == 160.0

def test_skycaller_resources() -> None:
    """Test resource calculation for Skycaller."""
    resources = Skycaller.total_basic_resources()
    assert resources["Salvage"] == 1270.0
    assert resources["Coal"] == pytest.approx(907.5)
    assert resources["Sulfur"] == 160.0

def test_king_jester_resources() -> None:
    """Test resource calculation for King_Jester."""
    resources = King_Jester.total_basic_resources()
    assert resources["Salvage"] == 2270.0
    assert resources["Coal"] == pytest.approx(2190.1)
    assert resources["Sulfur"] == 360.0
    assert resources["Rare Metals"] == 20.0

def test_mg_bt_resources() -> None:
    """Test resource calculation for MG_BT."""
    resources = MG_BT.total_basic_resources()
    assert resources["Salvage"] == 63450.0
    assert resources["Coal"] == pytest.approx(65582.0)
    assert resources["Sulfur"] == 9900.0

def test_flame_bt_resources() -> None:
    """Test resource calculation for Flame_BT."""
    resources = Flame_BT.total_basic_resources()
    assert resources["Salvage"] == 69975.0
    assert resources["Coal"] == pytest.approx(80646.5)
    assert resources["Sulfur"] == 11800.0

def test_spg_resources() -> None:
    """Test resource calculation for SPG."""
    resources = SPG.total_basic_resources()
    assert resources["Salvage"] == 151975.0
    assert resources["Coal"] == pytest.approx(163592.0)
    assert resources["Sulfur"] == 25600.0

def test_rsc_resources() -> None:
    """Test resource calculation for RSC."""
    resources = RSC.total_basic_resources()
    assert resources["Salvage"] == 296375.0
    assert resources["Coal"] == pytest.approx(224424.75)
    assert resources["Sulfur"] == 37900.0
    assert resources["Rare Metals"] == 2000.0

def test_storm_cannon_resources() -> None:
    """Test resource calculation for StormCannon."""
    resources = StormCannon.total_basic_resources()
    assert resources["Salvage"] == 121350.0
    assert resources["Coal"] == pytest.approx(23322.75)
    assert resources["Rare Metals"] == 800.0

def test_underground_fortress_resources() -> None:
    """Test resource calculation for UndergroundFortress."""
    resources = UndergroundFortress.total_basic_resources()
    assert resources["Salvage"] == 40350.0
    assert resources["Coal"] == pytest.approx(363.0)
    assert resources["Rare Metals"] == 100.0

def test_intel_center_resources() -> None:
    """Test resource calculation for IntelCenter."""
    resources = IntelCenter.total_basic_resources()
    assert resources["Salvage"] == 62550.0
    assert resources["Coal"] == pytest.approx(20636.55)
    assert resources["Rare Metals"] == 60.0

def test_frigate_resources() -> None:
    """Test resource calculation for Frigate."""
    resources = Frigate.total_basic_resources()
    assert resources["Salvage"] == 139440.0
    assert resources["Coal"] == pytest.approx(5662.8)
    assert resources["Rare Metals"] == 960.0

def test_warden_submarine_resources() -> None:
    """Test resource calculation for Warden_Submarine."""
    resources = Warden_Submarine.total_basic_resources()
    assert resources["Salvage"] == 174300.0
    assert resources["Coal"] == pytest.approx(7078.5)
    assert resources["Rare Metals"] == 1200.0

def test_firebrand_resources() -> None:
    """Test resource calculation for Firebrand."""
    resources = Firebrand.total_basic_resources()
    assert resources["Salvage"] == 1875.0
    assert resources["Sulfur"] == 300.0

def test_bowhead_resources() -> None:
    """Test resource calculation for Bowhead."""
    resources = Bowhead.total_basic_resources()
    assert resources["Salvage"] == 95040.0
    assert resources["Coal"] == pytest.approx(3775.2)
    assert resources["Rare Metals"] == 640.0

def test_longhook_resources() -> None:
    """Test resource calculation for Longhook (inherits from Bowhead)."""
    resources = Longhook.total_basic_resources()
    assert resources["Salvage"] == 95040.0
    assert resources["Coal"] == pytest.approx(3775.2)
    assert resources["Rare Metals"] == 640.0

def test_bluefin_resources() -> None:
    """Test resource calculation for Bluefin."""
    resources = Bluefin.total_basic_resources()
    assert resources["Salvage"] == 290500.0
    assert resources["Rare Metals"] == 2000.0
