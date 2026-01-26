from typing import Type, Any, Union, cast
from products import *
from products import (
    Outlaw, Chieftain, Thornfall, Blinder, Skycaller, RAC, KingJester, Flame_BT, MG_BT, SPG, 
    StormCannon, IntelCenter, UndergroundFortress, RSC, Sub, Frigate, Bluefin, Longhook, Bowhead, Prod
)
from functions import pick_products, is_exit_key, user_nums, is_user_input_in_map, calculate_total_resources, get_mats
# TODO: have user be able to have multiple instances of same object


Products: dict[str, Type[Prod]] = {
    "Outlaw": Outlaw,
    "Chieftain": Chieftain,
    "Thornfall": Thornfall,
    "ATHT": Blinder,
    "Skycaller": Skycaller,
    "RAC": RAC,
    "King Jester": KingJester,
    "Flame BT": Flame_BT,
    "MG BT": MG_BT,
    "SPG": SPG,
    "SC": StormCannon,
    "IC": IntelCenter,
    "UF": UndergroundFortress,
    "RSC": RSC,
    "Sub": Sub,
    "Frigate": Frigate,
    "Bluefin": Bluefin,
    "Longhook": Longhook,
    "Bowhead": Bowhead
}
# create second dict of lowercase keys that correspond to Products keys ('rsc': 'RSC')
lowercase_product_map: dict[str, str] = {k.lower(): k for k in Products}
list_of_products = list(Products.keys())
users_map_of_products: dict[str, int] = dict()

def main_loop() -> None:
    print("Type 1 if you want to have total materials displayed too.\n>> ")
    wants_mat_cost = input()

    while True:
        print("Type: 'done' to skip to start calculation or exit")
        choice = pick_products(list_of_products, lowercase_product_map)
        if choice not in list_of_products and choice != 'done':
            print(f"Invalid choice. Please choose from {list_of_products}.")
            continue
        if is_exit_key(choice):
            break
        # pick_number is int, but is_exit_key expects str. 
        # user_nums returns int. 
        # Logic issue here: user_nums handles its own input loop but returns int.
        # If user types "done" in user_nums, user_nums will raise ValueError or loop.
        # The original code `if is_exit_key(pick_number):` implies pick_number could be str?
        # Looking at functions.py, user_nums always returns int or recurses.
        # So `is_exit_key(pick_number)` is type error and logic error.
        pick_number = user_nums(choice)
        
        # Checking logic: user_nums doesn't return 'done'.
        # Removing the is_exit_key check on pick_number as it's unreachable/incorrect type.
        
        if is_user_input_in_map(choice, Products):
            users_map_of_products[choice] = pick_number
            print(f"You chose: {pick_number} {choice}")
        else:
            print("Something went wrong, exiting the loop")
            break

    print(f"Calculating resources needed for {users_map_of_products}\n")
    total = calculate_total_resources(users_map_of_products, Products)

    total_mats: Union[dict[str, float], str]
    if wants_mat_cost == "1":
        total_mats = get_mats(users_map_of_products, Products)
    else:
        total_mats = "N/A"
    
    print("Total resources needed: ", total)
    print("Total Facility Materials needed: ", total_mats)



if __name__ == "__main__":
    main_loop()
