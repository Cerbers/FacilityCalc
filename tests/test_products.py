import pytest
from products import Chieftain, Outlaw, Bluefin

def test_chieftain_resources():
    # Chieftain cost:
    # PCmat: 5 -> 5 * 100 Salvage = 500
    # A1: 10   -> 10 * 15 Salvage = 150, 10 * 90.75 Coal = 907.5
    # A4: 8    -> 8 * 100 Salvage = 800
    
    # Total Salvage = 500 + 150 + 800 = 1450
    # Total Coal = 907.5
    
    resources = Chieftain.total_basic_resources()
    assert resources["Salvage"] == 1450
    assert resources["Coal"] == pytest.approx(907.5)

def test_outlaw_resources():
    # Outlaw cost:
    # PCmat: 10 -> 1000 Salvage
    # A1: 10    -> 150 Salvage, 907.5 Coal
    # A4: 10    -> 1000 Salvage
    
    # Total Salvage = 1000 + 150 + 1000 = 2150
    # Total Coal = 907.5
    
    resources = Outlaw.total_basic_resources()
    assert resources["Salvage"] == 2150
    assert resources["Coal"] == pytest.approx(907.5)

def test_bluefin_resources():
    # Bluefin cost:
    # NavalPlate: 25
    # NavalHull: 25
    
    # NavalPlate cost: Cmat: 2, Thermal: 1
    #   Cmat: 2 -> 10 Salvage
    #   Thermal cost: Cmat: 2, A4: 5
    #     Cmat: 2 -> 10 Salvage
    #     A4: 5 -> 5 * 100 = 500 Salvage
    #     Thermal total -> 510 Salvage
    #   NavalPlate total -> 10 + 510 = 520 Salvage
    
    # NavalHull cost: PCmat: 60, A1: 2, A2: 2, A4: 10, RareAlloy: 4, Thermal: 4
    #   PCmat: 60 -> 6000 Salvage
    #   A1: 2 -> 30 Salvage, 2 * 90.75 = 181.5 Coal
    #   A2: 2 -> 2 * 15 = 30 Salvage
    #   A4: 10 -> 1000 Salvage
    #   RareAlloy: 4 -> Rare Metals: 20*4=80, PCmat: 5*4=20->2000 Salvage, Coke: 60*4=240->290.4 Coal
    #   Thermal: 4 -> 4 * 510 = 2040 Salvage
    
    #   NavalHull Total Salvage = 6000 + 30 + 30 + 1000 + 2000 + 2040 = 11100
    #   NavalHull Total Coal = 181.5 + 290.4 = 471.9
    #   NavalHull Total Rare Metals = 80
    
    # Bluefin Total:
    #   NavalPlate (25): 25 * 520 = 13000 Salvage
    #   NavalHull (25): 25 * 11100 = 277500 Salvage, 25 * 471.9 Coal, 25 * 80 Rare Metals
    
    #   Total Salvage = 13000 + 277500 = 290500
    #   Total Rare Metals = 2000
    
    resources = Bluefin.total_basic_resources()
    assert resources["Salvage"] == 290500
    assert resources["Rare Metals"] == 2000
