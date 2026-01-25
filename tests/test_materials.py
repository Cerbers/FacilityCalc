import pytest
from materials import Coke, Cmat, PCmat, Steel, A1, A5

def test_coke_basic_resources():
    # Coke cost: Coal: 1.21
    resources = Coke.total_basic_resources()
    assert resources == {"Coal": 1.21}

def test_cmat_basic_resources():
    # Cmat cost: Salvage: 5
    resources = Cmat.total_basic_resources()
    assert resources == {"Salvage": 5}

def test_pcmat_basic_resources():
    # PCmat cost: Cmat: 15, Salvage: 25
    # Cmat is 5 Salvage.
    # Total Salvage = 15 * 5 + 25 * 1 = 100
    resources = PCmat.total_basic_resources()
    assert resources == {"Salvage": 100}

def test_steel_basic_resources():
    # Steel cost: PCmat: 3, Coke: 125, Sulfur: 60
    # PCmat -> 100 Salvage
    # Coke -> 1.21 Coal
    # Sulfur -> 1 Sulfur (basic)
    
    # Total:
    # Salvage: 3 * 100 = 300
    # Coal: 125 * 1.21 = 151.25
    # Sulfur: 60 * 1 = 60
    
    resources = Steel.total_basic_resources()
    assert resources["Salvage"] == 300
    assert resources["Sulfur"] == 60
    assert resources["Coal"] == pytest.approx(151.25)

def test_a1_basic_resources():
    # A1 cost: Salvage: 15, Coke: 75
    # Coke -> 1.21 Coal
    # Total:
    # Salvage: 15
    # Coal: 75 * 1.21 = 90.75
    
    resources = A1.total_basic_resources()
    assert resources["Salvage"] == 15
    assert resources["Coal"] == pytest.approx(90.75)
