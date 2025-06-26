from products import *

# TODO: have user be able to have multiple instances of same object

basic_resources = ("Salvage", "Coal", "Sulfur")


Products = {
    "Outlaw": Outlaw,
    "Chieftain": Chieftain,
    "Thornfall": Thornfall,
    "ATHT": Blinder,
    "Skycaller": Skycaller,
    "RAC": RAC,
    "King Jester": KingJester,
    "MG BT": MG_BT,
    "SPG": SPG,
    "SC": StormCannon,
    "IC": IntelCenter,
    "UF": UndergroundFortress,
    "RSC": RSC
}
# create second dict of lowercase keys that correspond to Products keys ('rsc': 'RSC')
lowercase_product_map = {k.lower(): k for k in Products}

list_of_products = list(Products.keys())

def pick_products():
    user_input = input(f"Choose a vehicle {list_of_products}: ").strip()
    # take user input string and make it lower case then call the lowercase dict to invoke the correct KEY
    key = lowercase_product_map.get(user_input.lower())
    if key:
        return key  # Return the correctly-cased product name
    return user_input  # Return as-is if not found (so your error handling still works)


def is_exit_key(inp):
    return inp == "done"

def user_nums(x):
    try:
        quantity = int(input(f"How many {x} do you want to build?\n>> "))
        return quantity
    except ValueError:
        print("Not a number, type a number.\n")
        return user_nums(x)

def calculate_total_resources(users_map_of_products, Products):
    total = dict() 
    # itarate over products picked by user and get
    for product_name, amount in users_map_of_products.items():
        product_picked = Products[product_name]
        # checks if the object has the necessary attr
        if hasattr(product_picked, 'total_basic_resources'):
            # throws the return of the method in resources
            resources = product_picked.total_basic_resources()
            # multiplies each value by set amount in users_map value
            resources = {k: v * amount for k, v in resources.items()}
            print(f"{product_name} x{amount}: {resources}\n")
            get_resources_from_key(resources, total)
    return total

def get_resources_from_key(map, ref):
    # sums resources for each product
    for k, v in map.items():
        ref[k] = ref.get(k, 0) + v
    return ref[k]



def main_loop():
    while True:
        users_map_of_products = dict()
        while True:
            print("type: 'done' to skip to start calculation or exit")
            choice = pick_products()
            if choice not in list_of_products and choice != 'done':
                print(f"Invalid choice. Please choose from {list_of_products}.")
                continue
            if is_exit_key(choice):
                break
            pick_number = user_nums(choice)
            if is_exit_key(pick_number):
                break
            if choice in Products:
                users_map_of_products[choice] = pick_number
                print(f"You chose: {pick_number} {choice}")
        print(f"Calculating resources needed for {users_map_of_products}\n")
        total = calculate_total_resources(users_map_of_products, Products)
        print("Total resources needed: ", total)
        break


if __name__ == "__main__":
    main_loop()

