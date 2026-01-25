def iterate_and_multiply_keys(map: dict, result: dict, qty: int) -> dict:
    for k, v in map.items():
            result[k] = result.get(k, 0) + int(v) * qty
    return result


def pick_products(list: list, map: dict):
    user_input = input(f"Choose a vehicle {list}: \n>> ").strip()
    # take user input string and make it lower case then call the lowercase dict to invoke the correct KEY
    key = map.get(user_input.lower())
    if key:
        return key  # Return the correctly cased product name
    return user_input


def is_exit_key(inp: str):
    return inp == "done"


def user_nums(x: int) -> int:
    try:
        quantity = int(input(f"How many {x} do you want to build?\n>> "))
        return quantity
    except ValueError:
        print("Not a number, type a number.\n")
        return user_nums(x)


def is_user_input_in_map(x, map):
    return x in map


def calculate_total_resources(users_map_of_products: dict, Products: dict) -> dict:
    total = dict() 
    # iterate over products picked by user and get their true key
    for product_name, amount in users_map_of_products.items():
        product_picked = Products[product_name]
        if hasattr(product_picked, 'total_basic_resources'):
            # throws the return of the method in resources
            resources = product_picked.total_basic_resources()
            # multiplies each value by set amount in users_map value
            resources = {k: v * amount for k, v in resources.items()}
            print(f"{product_name} x{amount}: {resources}\n")
            sum_resources_from_each_product(resources, total)
    return total


def sum_resources_from_each_product(map, ref):
    for k, v in map.items():
        ref[k] = ref.get(k, 0) + v
    return ref[k]


def get_mats(users_map_of_products, Products):
    total = dict() 
    # iterate over products picked by user and get their true key
    for product_name, amount in users_map_of_products.items():
        product_picked = Products[product_name]
        if hasattr(product_picked, 'cost'):
            materials = product_picked.cost
            materials = {k: v * amount for k, v in materials.items()}
            print(f"{product_name} x{amount}: {materials}\n")
            sum_resources_from_each_product(materials, total)
    return total
