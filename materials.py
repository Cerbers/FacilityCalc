from typing import Any, Type
from functions import iterate_and_multiply_keys

basic_resources: tuple[str, ...] = ("Salvage", "Coal", "Sulfur", "Rare Metals") # reminder of what the objects are breakdowned to

class Material:
    cost: dict[str, float] = {}
    
    @classmethod
    def total_basic_resources(cls) -> dict[str, float]:
            if not cls.cost:
                raise ValueError(f"No attributies in cost dictionary in {cls.__name__}")
            total: dict[str, float] = {}
            for mat_name, qty in cls.cost.items():
                mat = materials_map.get(mat_name)
                if mat and hasattr(mat, "total_basic_resources"):
                    resources = mat.total_basic_resources()
                else:
                    resources = {mat_name: 1.0}
                iterate_and_multiply_keys(resources, total, qty)
            return total

class Coke(Material):
    cost = {
        "Coal": 1.21
    }

class Cmat(Material):
    cost = {
        "Salvage": 5.0
    }

class PCmat(Material):
    cost = {
        "Cmat": 15.0,
        "Salvage": 25.0 # this is a innacurate value, in place of 'metal beam'
    }

class A1(Material):
    cost = {
        "Salvage": 15.0,
        "Coke": 75.0
    }

class A2(Material):
    cost = {
        "Salvage": 15.0
    }

class A3(Material):
    cost = {
        "Cmat": 3.0,
        "Sulfur": 20.0
    }

class A4(Material):
    cost = {
        "PCmat": 1.0
    }

class Steel(Material):
    cost = {
        "PCmat": 3.0,
        "Coke": 125.0,
        "Sulfur": 60.0
    }

class A5(Material):
    cost = {
        "Steel": 3.0,
        "Coke": 245.0,
        "A1": 10.0,
        "A2": 10.0
    }
    
class RareAlloy(Material):
    cost = {
        "Rare Metals": 20.0,
        "PCmat": 5.0,
        "Coke": 60.0
    }

class ThermalShielding(Material):
    cost = {
        "Cmat": 2.0,
        "A4": 5.0
    }

class NavalShellPlating(Material):
    cost = {
        "Cmat": 2.0,
        "Thermal": 1.0
    }

class NavalHullSegment(Material):
    cost = {
        "PCmat": 60.0,
        "A1": 2.0,
        "A2": 2.0,
        "A4": 10.0,
        "RareAlloy": 4.0,
        "Thermal": 4.0
    }

class ConstructionPart(Material):
    cost = {
        "PCmat": 250.0,
        "A1": 225.0,
        "A2": 225.0
    }

class StructurePart(Material):
    cost = {
        "PCmat": 50.0,
        "A4": 40.0,
        "Thermal": 15.0
    }

class StormCannonPart(Material):
    cost = {
        "PCmat": 300.0,
        "RareAlloy": 40.0,
        "Thermal": 45.0
    }

class IntelCenterPart(Material):
    cost = {
        "PCmat": 50.0,
        "RareAlloy": 3.0,
        "Thermal": 15.0
    }

materials_map: dict[str, Type[Material]] = {
    "Cmat": Cmat,
    "Coke": Coke,
    "PCmat": PCmat,
    "A1": A1,
    "A2": A2,
    "A3": A3,
    "A4": A4,
    "A5": A5,
    "Steel": Steel,
    "RareAlloy": RareAlloy,
    "Thermal": ThermalShielding,
    "NavalPlate": NavalShellPlating,
    "NavalHull": NavalHullSegment,
    "CP": ConstructionPart,
    "SP": StructurePart,
    "SCP": StormCannonPart,
    "ICP": IntelCenterPart
}
