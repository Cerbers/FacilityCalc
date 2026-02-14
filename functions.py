from typing import Any, Union

def iterate_and_multiply_keys(data_map: dict[str, float], result: dict[str, float], qty: Union[int, float]) -> dict[str, float]:
    for k, v in data_map.items():
            result[k] = result.get(k, 0.0) + v * qty
    return result


def calculate_total_basic_resources(cost: dict[str, float], materials_map: dict[str, Any]) -> dict[str, float]:
    if not cost:
        raise ValueError("No attributes in cost dictionary")
    total: dict[str, float] = {}
    for mat_name, qty in cost.items():
        mat = materials_map.get(mat_name)
        if mat and hasattr(mat, "total_basic_resources"):
            resources = mat.total_basic_resources()
        else:
            resources = {mat_name: 1.0}
        iterate_and_multiply_keys(resources, total, qty)
    return total


def pick_products(options_list: list[str], data_map: dict[str, str], prompt_text: str = "") -> str:
    if prompt_text is not "":
        user_input = input(prompt_text).strip()
    else:
        user_input = input(f"Choose a vehicle {options_list}: \n>> ").strip()
    # take user input string and make it lower case then call the lowercase dict to invoke the correct KEY
    key = data_map.get(user_input.lower())
    if key:
        return key  # Return the correctly cased product name
    return user_input


def is_exit_key(input: str) -> bool:
    return input == "done"


def get_build_quantity(product_name: str) -> int:
    try:
        quantity = int(input(f"How many {product_name} do you want to build?\n>> "))
        return quantity
    except ValueError:
        print("Not a number, type a number.\n")
        return get_build_quantity(product_name)


def is_user_input_in_map(x: str, data_map: dict[str, Any]) -> bool:
    return x in data_map


def calculate_total_resources(user_selections: list[tuple[str, int]], Products: dict[str, Any]) -> dict[str, float]:
    total: dict[str, float] = dict() 
    # iterate over products picked by user and get their true key
    for product_name, amount in user_selections:
        product_picked = Products[product_name]
        if hasattr(product_picked, 'total_basic_resources'):
            # throws the return of the method in resources
            resources: dict[str, float] = product_picked.total_basic_resources()
            # multiplies each value by set amount in users_map value
            resources = {k: v * amount for k, v in resources.items()}
            print(f"{product_name} x{amount}: { {k: int(v) for k, v in resources.items()} }\n")
            sum_resources_from_each_product(resources, total)
    return total


def sum_resources_from_each_product(data_map: dict[str, float], ref: dict[str, float]) -> None:
    for k, v in data_map.items():
        ref[k] = ref.get(k, 0.0) + v



def get_materials(user_selections: list[tuple[str, int]], Products: dict[str, Any]) -> dict[str, float]:
    total: dict[str, float] = dict() 
    # iterate over products picked by user and get their true key
    for product_name, amount in user_selections:
        product_picked = Products[product_name]
        if hasattr(product_picked, 'cost'):
            materials: dict[str, float] = product_picked.cost
            materials = {k: v * amount for k, v in materials.items()}
            print(f"{product_name} x{amount}: { {k: int(v) for k, v in materials.items()} }\n")
            sum_resources_from_each_product(materials, total)
    return total
