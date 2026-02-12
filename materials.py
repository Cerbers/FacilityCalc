from typing import Type
from functions import iterate_and_multiply_keys

basic_resources: tuple[str, ...] = ("Salvage", "Coal", "Sulfur", "Rare Metals", "Components") # reminder of what the objects are breakdowned to

class Material:
    cost: dict[str, float] = {}
    recipes: dict[str, dict[str, float]] = {}
    current_recipe: str = ""

    @classmethod
    def set_recipe(cls, recipe_name: str) -> None:
        if recipe_name not in cls.recipes:
            raise ValueError(
                f"Unknown recipe '{recipe_name}' for {cls.__name__}. "
                f"Available: {list(cls.recipes.keys())}"
            )
        cls.cost = cls.recipes[recipe_name]
        cls.current_recipe = recipe_name

    @classmethod
    def total_basic_resources(cls) -> dict[str, float]:
            if not cls.cost:
                raise ValueError(f"No attributes in cost dictionary in {cls.__name__}")
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
    recipes = {
        "Coal Refinery Basic": {"Coal": 1.11},
        "Coke Furnace": {"Coal": 1.21},
        "Advanced Coal Liquefier (+Heavy Oil)": {"Coal": 1.15},
    }
    cost = recipes["Coke Furnace"]
    current_recipe = "Coke Furnace"

class Cmat(Material):
    recipes = {
        "Material Factory": {"Salvage": 10.0},
        "Assembly Bay": {"Salvage": 25.0},
        "Metal Press (+Petrol)": {"Salvage": 5.0},
        "Smelter": {"Salvage": 5.0, "Coke": 8.333},
    }
    cost = recipes["Metal Press (+Petrol)"]
    current_recipe = "Metal Press (+Petrol)"

class PCmat(Material):
    recipes = {
        "Metalworks": {"Cmat": 3.0, "Components": 20.0},
        "Blast Furnace (+Heavy Oil)": {"Cmat": 1.0, "Components": 18.333},
        "Recycler": {"Cmat": 15.0, "Salvage": 25.0},  # Salvage in place of 'metal beam'
    }
    cost = recipes["Recycler"]
    current_recipe = "Recycler"

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

class EnrichedOil(Material):
    recipes = {
        "Oil Refinery (+Heavy Oil)": {"Sulfur": 60.0},
        "Offshore Platform": {"Coal": 100.0},
    }
    cost = recipes["Oil Refinery (+Heavy Oil)"]
    current_recipe = "Oil Refinery (+Heavy Oil)"

class Steel(Material):
    recipes = {
        "Default": {"PCmat": 3.0, "Coke": 125.0, "Sulfur": 60.0},
        "Heavy Oil (+Heavy Oil)": {"PCmat": 3.0, "Coke": 200.0, "Sulfur": 65.0},
        "Enriched Oil": {"PCmat": 3.0, "Coke": 125.0, "EnrichedOil": 1.0},
    }
    cost = recipes["Default"]
    current_recipe = "Default"

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

class NavalTurbine(Material):
    cost = {
        "A5": 20.0,
        "RareAlloy": 20.0
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
        "RareAlloy": 20.0,
        "Thermal": 45.0
    }

class IntelCenterPart(Material):
    cost = {
        "PCmat": 50.0,
        "RareAlloy": 3.0,
        "Thermal": 15.0
    }

class UndergroundFortressPart(Material):
    cost = {
        "PCmat": 200.0,
        "RareAlloy": 5.0,
        "Thermal": 35.0
    }

class AircraftMechanicalPartsSmall(Material):
    cost = {
        "PCmat": 35.0,
        "A3": 25.0
    }

class AircraftEngineSmall(Material):
    cost = {
        "PCmat": 95.0,
        "A4": 25.0
    }

class AircraftEngineLarge(Material):
    cost = {
        "PCmat": 95.0,
        "A4": 25.0
    }

class AircraftMechanicalPartsLarge(Material):
    cost = {
        "PCmat": 35.0,
        "A3": 25.0
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
    "EnrichedOil": EnrichedOil,
    "RareAlloy": RareAlloy,
    "Thermal": ThermalShielding,
    "NavalPlate": NavalShellPlating,
    "NavalTurbine": NavalTurbine,
    "NavalHull": NavalHullSegment,
    "CP": ConstructionPart,
    "SP": StructurePart,
    "SCP": StormCannonPart,
    "ICP": IntelCenterPart,
    "UFP": UndergroundFortressPart,
    "AMPs": AircraftMechanicalPartsSmall,
    "AMPl": AircraftMechanicalPartsLarge,
    "AEs": AircraftEngineSmall,
    "AEl": AircraftEngineLarge
}

def get_switchable_materials() -> dict[str, Type[Material]]:
    """Return materials that have alternative recipes."""
    return {name: cls for name, cls in materials_map.items() if cls.recipes}
