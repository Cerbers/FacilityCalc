from typing import Type, Union
from products import Prod, name_mappings
from vehicle_groups import Warden, Colonial, All
from functions import pick_products, is_exit_key, get_build_quantity, is_user_input_in_map, calculate_total_resources, get_materials



Products: dict[str, Type[Prod]] = {**Warden, **Colonial, **All}
# Use name_mappings from products module which includes all aliases
list_of_products = list(Products.keys())


def main_loop() -> None:
    print("Type 1 if you want to have total materials displayed too.\n>> ")
    wants_mat_cost = input()

    user_selections: list[tuple[str, int]] = []

    while True:
        print("Type: 'done' to skip to start calculation or exit")
        choice = pick_products(list_of_products, name_mappings)
        if choice not in list_of_products and choice != 'done':
            print(f"Invalid choice. Please choose from {list_of_products}.")
            continue
        if is_exit_key(choice):
            break
        pick_number = get_build_quantity(choice)
        
        
        if is_user_input_in_map(choice, Products):
            user_selections.append((choice, pick_number))
            print(f"You chose: {pick_number} {choice}")
        else:
            print("Something went wrong, exiting the loop")
            break

    print(f"Calculating resources needed for {user_selections}\n")
    total = calculate_total_resources(user_selections, Products)

    total_mats: Union[dict[str, float], str]
    if wants_mat_cost == "1":
        total_mats = get_materials(user_selections, Products)
    else:
        total_mats = "N/A"
    
    print("Total resources needed: ", {k: int(v) for k, v in total.items()})
    
    if isinstance(total_mats, dict):
        print("Total Facility Materials needed: ", {k: int(v) for k, v in total_mats.items()})
    else:
        print("Total Facility Materials needed: ", total_mats)



if __name__ == "__main__":
    main_loop()
