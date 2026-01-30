from typing import Type
import products
from products import Prod

Warden: dict[str, Type[Prod]] = {}
Colonial: dict[str, Type[Prod]] = {}
All: dict[str, Type[Prod]] = {}

def _initialize_groups() -> None:
    # Iterate over all attributes in products module to find Prod subclasses
    for name, obj in vars(products).items():
        if isinstance(obj, type) and issubclass(obj, Prod) and obj is not Prod:
            # The class should have 'faction' attribute due to our changes in products.py
            # and _load_products validation
            if not hasattr(obj, 'faction'):
                continue
                
            faction = obj.faction.lower()
            
            # Use the class name as the key
            # If aliases are needed, they should be added to the JSON and handled here
            if faction == 'warden':
                Warden[name] = obj
            elif faction == 'colonial':
                Colonial[name] = obj
            elif faction == 'all':
                All[name] = obj

_initialize_groups()
