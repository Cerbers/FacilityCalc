basic_resources = ("Salvage", "Coal", "Sulfur", "Rare Metals") # reminder of what the objects are breakdowned to
from functions import iterate_andMultiply_keys


class Material:
    cost = {}
    @classmethod
    def total_basic_resources(cls):
            total = {}
            for mat_name, qty in cls.cost.items():
                mat = mat_map.get(mat_name) # Get the material object from mat_map
                if hasattr(mat, "total_basic_resources"):
                    # Recursively get the basic resources for this material
                    resources = mat.total_basic_resources()
                else:
                    resources = {mat_name: 1}
                # Multiply each resource by the quantity needed
                iterate_andMultiply_keys(resources, total, qty)
            return total

class Coke(Material):
    cost = {
        "Coal": 1.21
    }
    @classmethod
    def total_basic_resources(cls):
            total = {}
            for mat_name, qty in cls.cost.items():
                mat = mat_map.get(mat_name) # Get the material object from mat_map
                if hasattr(mat, "total_basic_resources"):
                    # Recursively get the basic resources for this material
                    resources = mat.total_basic_resources()
                else:
                    resources = {mat_name: 1}
                # Multiply each resource by the quantity needed
                iterate_andMultiply_keys(resources, total, qty)
            return total

class Cmat(Material):
    cost = {
        "Salvage": 5
    }

class PCmat(Material):
    cost = {
        "Cmat": 15,
        "Salvage": 25 # this is a innacurate value, in place of 'metal beam'
    }

class A1(Material):
    cost = {
        "Salvage": 15,
        "Coke": 75
    }

class A2(Material):
    cost = {
        "Salvage": 15
    }

class A3(Material):
    cost = {
        "Cmat": 3,
        "Sulfur": 20
    }

class A4(Material):
    cost = {
        "PCmat": 1
    }

class Steel(Material):
    cost = {
        "PCmat": 3,
        "Coke": 125,
        "Sulfur": 60
    }

class A5(Material):
    cost = {
        "Steel": 3,
        "Coke": 245,
        "A1": 10,
        "A2": 10
    }
    
class RareAlloy(Material):
    cost = {
        "Rare Metals": 20,
        "PCmat": 5,
        "Coke": 60
    }

class ThermalShielding(Material):
    cost = {
        "Cmat": 2,
        "A4": 5
    }

class NavalShellPlating(Material):
    cost = {
        "Cmat": 2,
        "Thermal": 1
    }

class NavalHullSegment(Material):
    cost = {
        "PCmat": 60,
        "A1": 2,
        "A2": 2,
        "A4": 10,
        "RareAlloy":4,
        "Thermal": 4
    }

class ConstructionPart(Material):
    cost = {
        "PCmat": 250,
        "A1": 225,
        "A2": 225
    }

class StructurePart(Material):
    cost = {
        "PCmat": 50,
        "A4": 40,
        "Thermal": 15
    }

class StormCannonPart(Material):
    cost = {
        "PCmat": 300,
        "RareAlloy": 40,
        "Thermal": 45
    }

class IntelCenterPart(Material):
    cost = {
        "PCmat": 50,
        "RareAlloy": 3,
        "Thermal": 15
    }

mat_map = {
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
