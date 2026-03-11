from typing import Type
import json
import os
from functions import iterate_and_multiply_keys, calculate_total_basic_resources

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
    def total_basic_resources(cls, depth: int = 0) -> dict[str, float]:
        if not cls.cost:
            raise ValueError(f"No attributes in cost dictionary in {cls.__name__}")
        return calculate_total_basic_resources(cls.cost, materials_map, depth)

class Coke(Material):
    recipes = {
        "Coal Refinery Basic": {"Coal": 1.11},
        "Coke Furnace": {"Coal": 1.21},
        "Advanced Coal Liquefier": {"Coal": 1.15},
    }
    cost = recipes["Coke Furnace"]
    current_recipe = "Coke Furnace"

class Cmat(Material):
    recipes = {
        "Material Factory": {"Salvage": 10.0},
        "Assembly Bay": {"Salvage": 25.0},
        "Metal Press": {"Salvage": 5.0},
        "Smelter": {"Salvage": 5.0, "Coke": 8.333},
    }
    cost = recipes["Metal Press"]
    current_recipe = "Metal Press"

class PCmat(Material):
    recipes = {
        "Metalworks": {"Cmat": 3.0, "Components": 20.0},
        "Blast Furnace": {"Cmat": 1.0, "Components": 18.333},
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
        "Oil Refinery": {"Sulfur": 60.0},
        "Offshore Platform": {"Coal": 100.0},
    }
    cost = recipes["Oil Refinery"]
    current_recipe = "Oil Refinery"

class Steel(Material):
    recipes = {
        "Default": {"PCmat": 3.0, "Coke": 125.0, "Sulfur": 60.0},
        "Heavy Oil": {"PCmat": 3.0, "Coke": 200.0, "Sulfur": 65.0},
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


def load_recipe_preferences() -> None:
    """Load recipe preferences from JSON file if it exists."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prefs_path = os.path.join(current_dir, "recipe_preferences.json")

    if not os.path.exists(prefs_path):
        return

    try:
        with open(prefs_path, "r") as f:
            prefs = json.load(f)

        if not isinstance(prefs, dict):
            print(f"Warning: preferences file is not a valid JSON object, using defaults")
            return

        for mat_name, recipe_name in prefs.items():
            if not isinstance(mat_name, str):
                print(f"Warning: Skipping invalid material name '{mat_name}', using defaults")
                continue

            mat_class = materials_map.get(mat_name)

            if not mat_class:
                print(f"Warning: Unknown material '{mat_name}' in preferences, using defaults")
                continue

            if not mat_class.recipes:
                print(f"Warning: Material '{mat_name}' has no recipes, using defaults")
                continue

            if not isinstance(recipe_name, str):
                print(f"Warning: Invalid recipe '{recipe_name}' for '{mat_name}', using defaults")
                continue

            try:
                mat_class.set_recipe(recipe_name)
            except ValueError as e:
                print(f"Warning: {e}")

    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Failed to load preferences: {e}")
