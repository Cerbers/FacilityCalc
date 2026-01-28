from typing import Any
import json
import os
import materials as mats
from functions import iterate_and_multiply_keys

# TODO: Externalize products objects to a json file from which program will read them so the user can add/remove/change products without changing code



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

def _load_products():
    """Load products from JSON file and create classes dynamically."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'products.json')
    
    try:
        with open(json_path, 'r') as f:
            products_data = json.load(f)
            
        for name, cost_data in products_data.items():
            # Create class dynamically: type(name, bases, dict)
            # We inherit from Prod and set the 'cost' attribute
            cls = type(name, (Prod,), {'cost': cost_data})
            # Add the class to the module's global namespace
            globals()[name] = cls
            
    except FileNotFoundError:
        print(f"Warning: {json_path} not found. No products loaded.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode {json_path}.")

# Load products when module is imported
_load_products()
