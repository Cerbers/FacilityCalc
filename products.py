from typing import Any
import json
import os
import materials as mats
from functions import iterate_and_multiply_keys, calculate_total_basic_resources


class Prod:
    cost: dict[str, float] = {}
    faction: str = "all"
    names: list[str] = []

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        
        # Allow Prod base class itself to not have faction
        if cls.__name__ == 'Prod':
            return
        
        # All subclasses MUST have faction
        if not hasattr(cls, "faction") or not cls.faction:
             # This should default to "all" from base class if not set, but explicit check is fine
             pass
        
        # Validate faction value
        if cls.faction not in ["warden", "colonial", "all"]:
            raise ValueError(
                f"Invalid faction '{cls.faction}' for product '{cls.__name__}'. "
                f"Must be 'warden', 'colonial', or 'all'."
            )

    @classmethod
    def total_basic_resources(cls, depth: int = 0) -> dict[str, float]:
        if not cls.cost:
            raise ValueError(f"No attributes in cost dictionary in {cls.__name__}")
        return calculate_total_basic_resources(cls.cost, mats.materials_map, depth)

# Global dictionary to map all acceptable names to product names
name_mappings: dict[str, str] = {}

def _load_products() -> None:
    """Load products from JSON file and create classes dynamically."""
    global name_mappings
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
            
            cost_data = data["cost"]
            
            # Validate materials exist
            invalid_mats = [k for k in cost_data.keys() if k not in mats.materials_map]
            if invalid_mats:
                print(f"Warning: Skipping '{name}' - contains invalid materials: {invalid_mats}")
                continue

            # Handle faction - default to "all" if missing or empty
            faction = data.get("faction", "all")
            if not faction:
                faction = "all"
            
            # Validate faction value before class creation
            if faction not in ["warden", "colonial", "all"]:
                print(f"Warning: Skipping '{name}' - invalid faction '{faction}'")
                continue

            # Get names list - use product name as default if not specified
            names_list = data.get("names", [name])
            
            # Create class dynamically
            try:
                cls = type(name, (Prod,), {'cost': cost_data, 'faction': faction, 'names': names_list})
                globals()[name] = cls
                # Add all names to the global name_mappings dictionary
                for alias in names_list:
                    alias_lower = alias.lower()
                    if alias_lower in name_mappings:
                        print(f"Warning: Duplicate alias '{alias}' for product '{name}' (already maps to '{name_mappings[alias_lower]}')")
                    name_mappings[alias_lower] = name
            except ValueError as e:
                print(f"Error creating '{name}': {e}")
            
    except FileNotFoundError:
        print(f"Warning: {json_path} not found. No products loaded.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode {json_path}.")

# Load products when module is imported
_load_products()
