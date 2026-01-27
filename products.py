from typing import Any
import materials as mats
from functions import iterate_and_multiply_keys

# TODO: Externalize products objects to a json file from which program will read them so the user can add/remove/change products without changing code

# initializing materials
Coke = mats.Coke
Cmat = mats.Cmat
PCmat = mats.PCmat
A1 = mats.A1
A2 = mats.A2
A3 = mats.A3
A4 = mats.A4
Steel = mats.Steel
A5 = mats.A5
Rare_Alloy = mats.RareAlloy
Thermal = mats.ThermalShielding
NavalPlate =mats.NavalShellPlating
NavalHull = mats.NavalHullSegment
ConstructionPart = mats.ConstructionPart
StructurePart = mats.StructurePart
StormCannonPart = mats.StormCannonPart
IntelCenterPart = mats.IntelCenterPart



class Prod:
    cost: dict[str, float] = {}

    @classmethod
    def total_basic_resources(cls) -> dict[str, float]:
            if not cls.cost:
                raise ValueError(f"No attributies in cost dictionary in {cls.__name__}")
            total: dict[str, float] = {}
            for mat_name, qty in cls.cost.items():
                mat = mats.materials_map.get(mat_name)
                if mat and hasattr(mat, "total_basic_resources"):
                    resources = mat.total_basic_resources()
                else:
                    resources = {mat_name: 1.0}
                iterate_and_multiply_keys(resources, total, qty)
            return total

class Chieftain(Prod):
    cost = {
        "PCmat": 5.0,
        "A1": 10.0,
        "A4": 8.0
    }

class Thornfall(Prod):
    cost = {
        "PCmat": 60.0,
        "A4": 15.0,
        "A3": 15.0,
        "A1": 10.0
    }

class Outlaw(Prod):
    cost = {
        "PCmat": 10.0,
        "A1": 10.0,
        "A4": 10.0
    }

class Blinder(Prod):
    cost = {
        "PCmat": 5.0,
        "A2": 10.0,
        "A4": 3.0
    }

class RAC(Prod):
    cost = {
        "PCmat": 35.0,
        "A1": 10.0,
        "A3": 8.0
    }

class Skycaller(Prod):
    cost = {
        "PCmat": 10.0,
        "A1": 10.0,
        "A3": 8.0
    }

class King_Jester(Prod):
    cost = {
        "Steel": 5.0,
        "A1": 15.0,
        "A3": 3.0,
        "RareAlloy": 1.0
    }

class MG_BT(Prod):
    cost = {
        "Steel": 50.0,
        "A5": 35.0,
        "A4": 60.0,
        "A3": 30.0
    }

class Flame_BT(Prod):
    cost = {
        "Steel": 40.0,
        "A5": 45.0,
        "A4": 30.0,
        "A3": 65.0
    }

class SPG(Prod):
    cost = {
        "Steel": 150.0,
        "A5": 85.0,
        "A4": 40.0,
        "A3": 65.0
    }

class RSC(Prod):
    cost = {
        "Steel": 285.0,
        "A5": 105.0,
        "A4": 105.0,
        "A3": 95.0,
        "RareAlloy": 100.0,
        "Thermal": 45.0
    }

class StormCannon(Prod):
    cost = {
        "CP": 1.0,
        "SP": 1.0,
        "SCP": 1.0
    }

class UndergroundFortress(Prod):
    cost = {
        "PCmat": 200.0,
        "RareAlloy": 5.0,
        "Thermal": 35.0
    }

class IntelCenter(Prod):
    cost = {
        "CP": 1.0,
        "SP": 1.0,
        "ICP": 1.0
    }

class Frigate(Prod):
    cost = {
        "NavalPlate": 12.0,
        "NavalHull": 12.0
    }

class Warden_Submarine(Prod):
    cost = {
        "NavalPlate": 15.0,
        "NavalHull": 15.0
    }

class Firebrand(Prod):
    cost = {
        "PCmat": 15.0,
        "A2": 10.0,
        "A3": 15.0
    }

class Bowhead(Prod):
    cost = {
        "NavalPlate": 12.0,
        "NavalHull": 8.0
    }

class Longhook(Bowhead):
    pass

class Bluefin(Prod):
    cost = {
        "NavalPlate": 25.0,
        "NavalHull": 25.0
    }
