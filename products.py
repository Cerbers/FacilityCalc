import materials as mats
from functions import iterate_and_multiply_keys
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
    cost = {}

    @classmethod
    def total_basic_resources(cls):
            total = {}
            for mat_name, qty in cls.cost.items():
                mat = mats.materials_map.get(mat_name)
                if hasattr(mat, "total_basic_resources"):
                    resources = mat.total_basic_resources()
                else:
                    resources = {mat_name: 1}
                iterate_and_multiply_keys(resources, total, qty)
            return total

class Chieftain(Prod):
    cost = {
        "PCmat": 5,
        "A1": 10,
        "A4": 8
    }

class Thornfall(Prod):
    cost = {
        "PCmat": 60,
        "A4": 15,
        "A3": 15,
        "A1": 10
    }

class Outlaw(Prod):
    cost = {
        "PCmat": 10,
        "A1": 10,
        "A4": 10
    }

class Blinder(Prod):
    cost = {
        "PCmat": 5,
        "A2": 10,
        "A4": 3
    }

class RAC(Prod):
    cost = {
        "PCmat": 35,
        "A1": 10,
        "A3": 8
    }

class Skycaller(Prod):
    cost = {
        "PCmat": 10,
        "A1": 10,
        "A3": 8
    }

class KingJester(Prod):
    cost = {
        "Steel": 5,
        "A1": 15,
        "A3": 3,
        "RareAlloy": 1
    }

class MG_BT(Prod):
    cost = {
        "Steel": 50,
        "A5": 35,
        "A4": 60,
        "A3": 30
    }

class Flame_BT(Prod):
    cost = {
        "Steel": 40,
        "A5": 45,
        "A4": 30,
        "A3": 65
    }

class SPG(Prod):
    cost = {
        "Steel": 150,
        "A5": 85,
        "A4": 40,
        "A3": 65
    }

class RSC(Prod):
    cost = {
        "Steel": 285,
        "A5": 105,
        "A4": 105,
        "A3": 95,
        "RareAlloy": 100,
        "Thermal": 45
    }

class StormCannon(Prod):
    cost = {
        "CP": 1,
        "SP": 1,
        "SCP": 1
    }

class UndergroundFortress(Prod):
    cost = {
        "PCmat": 200,
        "RareAlloy": 5,
        "Thermal": 35
    }

class IntelCenter(Prod):
    cost = {
        "CP": 1,
        "SP": 1,
        "ICP": 1
    }

class Frigate(Prod):
    cost = {
        "NavalPlate": 12,
        "NavalHull": 12
    }

class Sub(Prod):
    cost = {
        "NavalPlate": 15,
        "NavalHull": 15
    }

class Bowhead(Prod):
    cost = {
        "NavalPlate": 12,
        "NavalHull": 8
    }

class Longhook(Bowhead):
    pass

class Bluefin(Prod):
    cost = {
        "NavalPlate": 25,
        "NavalHull": 25
    }
