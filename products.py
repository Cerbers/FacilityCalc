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
        if not hasattr(cls, "faction"):
            return # Should we allow subclasses without faction? The user requirement implies strictly checking.
            # But the dynamic creation will pass it. 
        
        # validation
        if cls.faction not in ["warden", "colonial", "all"]:
             raise ValueError(f"Invalid faction '{cls.faction}' for product '{cls.__name__}'. Must be 'warden', 'colonial', or 'all'.")

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
            # Check if data follows new schema (has 'faction' and 'cost')
            if "cost" in data and "faction" in data:
                 cost_data = data["cost"]
                 faction = data["faction"]
            else:
                 # Fallback for old schema or partial data - though we are updating json next.
                 # Let's assume strict new schema or just handle cost if it's the old one (but we will fail validation)
                 # Actually, let's just implement the new schema logic.
                 cost_data = data.get("cost", {})
                 faction = data.get("faction", "")

            # Create class dynamically: type(name, bases, dict)
            # We inherit from Prod and set the 'cost' and 'faction' attributes
            cls = type(name, (Prod,), {'cost': cost_data, 'faction': faction})
            # Add the class to the module's global namespace
            globals()[name] = cls
            
    except FileNotFoundError:
        print(f"Warning: {json_path} not found. No products loaded.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode {json_path}.")

# Load products when module is imported
_load_products()
