from products import *
from functions import *
# TODO: have user be able to have multiple instances of same object


Products = {
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
lowercase_product_map = {k.lower(): k for k in Products}
list_of_products = list(Products.keys())
users_map_of_products = dict()

def main_loop():
    while True:
        print("Type: 'done' to skip to start calculation or exit")
        choice = pick_products(list_of_products, lowercase_product_map)
        if choice not in list_of_products and choice != 'done':
            print(f"Invalid choice. Please choose from {list_of_products}.")
            continue
        if is_exit_key(choice):
            break
        pick_number = user_nums(choice)
        if is_exit_key(pick_number):
            break
        if is_userInput_in_map(choice, Products):
            users_map_of_products[choice] = pick_number
            print(f"You chose: {pick_number} {choice}")
        else:
            print("something went wrong, exiting the loop")
            break
    print(f"Calculating resources needed for {users_map_of_products}\n")
    total = calculate_total_resources(users_map_of_products, Products)
    print("Total resources needed: ", total)


if __name__ == "__main__":
    main_loop()
