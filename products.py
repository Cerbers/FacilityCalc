from typing import Any
import json
import os
import materials as mats
from functions import iterate_and_multiply_keys

# TODO: Externalize products objects to a json file from which program will read them so the user can add/remove/change products without changing code



class Prod:
    cost: dict[str, float] = {}
    faction: str

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        
        # Allow Prod base class itself to not have faction
        if cls.__name__ == 'Prod':
            return
        
        # All subclasses MUST have faction
        if not hasattr(cls, "faction") or not cls.faction:
            raise ValueError(
                f"Product '{cls.__name__}' must define a non-empty 'faction' attribute"
            )
        
        # Validate faction value
        if cls.faction not in ["warden", "colonial", "all"]:
            raise ValueError(
                f"Invalid faction '{cls.faction}' for product '{cls.__name__}'. "
                f"Must be 'warden', 'colonial', or 'all'."
            )

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

def _load_products():
    """Load products from JSON file and create classes dynamically."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'products.json')
    
    try:
        with open(json_path, 'r') as f:
            products_data = json.load(f)
            
        for name, data in products_data.items():
            # Validate required fields
            if "cost" not in data:
                print(f"Warning: Skipping '{name}' - missing 'cost' field")
                continue
            if "faction" not in data or not data["faction"]:
                print(f"Warning: Skipping '{name}' - missing or empty 'faction' field")
                continue
            
            cost_data = data["cost"]
            faction = data["faction"]
            
            # Validate faction value before class creation
            if faction not in ["warden", "colonial", "all"]:
                print(f"Warning: Skipping '{name}' - invalid faction '{faction}'")
                continue

            # Create class dynamically
            try:
                cls = type(name, (Prod,), {'cost': cost_data, 'faction': faction})
                globals()[name] = cls
            except ValueError as e:
                print(f"Error creating '{name}': {e}")
            
    except FileNotFoundError:
        print(f"Warning: {json_path} not found. No products loaded.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode {json_path}.")

# Load products when module is imported
_load_products()
