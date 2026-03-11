from typing import Any, Union

def iterate_and_multiply_keys(data_map: dict[str, float], result: dict[str, float], qty: Union[int, float]) -> dict[str, float]:
    """
    Multiplies each value in data_map by qty and stores the result in result dictionary.
    
    Args:
        data_map (dict[str, float]): Dictionary of values to be multiplied.
        result (dict[str, float]): Dictionary to store the result.
        qty (Union[int, float]): Quantity to multiply each value in data_map by.
    
    Returns:
        dict[str, float]: Dictionary with multiplied values.

    Example:
        data_map = {"a": 1.0, "b": 2.0}
        result = {}
        qty = 2.0
        iterate_and_multiply_keys(data_map, result, qty)
        # result = {"a": 2.0, "b": 4.0}
    """
    for k, v in data_map.items():
            result[k] = result.get(k, 0.0) + v * qty
    return result


def calculate_total_basic_resources(cost: dict[str, float], materials_map: dict[str, Any], depth: int = 0) -> dict[str, float]:
    """
    Calculates total basic resources needed for building products.

    Args:
        cost (dict[str, float]): Dictionary of materials needed for each product.
        materials_map (dict[str, Any]): Dictionary mapping material names to material classes.
        depth (int): Current recursion depth; raises RecursionError if it exceeds 10.

    Returns:
        dict[str, float]: Dictionary of total basic resources needed.

    Example:
        cost = {"PCmat": 100.0}
        materials_map = {"PCmat": PCmat}
        calculate_total_basic_resources(cost, materials_map)
        {"Salvage": 10000.0} // breakdown:
        PCmat>Cmat + Salvage> Salvage
    """
    if depth > 10:
        raise RecursionError(
            "Recursion depth exceeded (>10). Check products.json or materials.py "
            "for circular dependencies."
        )
    if not cost:
        raise ValueError("No attributes in cost dictionary")
    total: dict[str, float] = {}
    for mat_name, qty in cost.items():
        mat = materials_map.get(mat_name)
        if mat and hasattr(mat, "total_basic_resources"):
            resources = mat.total_basic_resources(depth + 1)
        else:
            resources = {mat_name: 1.0}
        iterate_and_multiply_keys(resources, total, qty)
    return total


def pick_products(options_list: list[str], data_map: dict[str, str], prompt_text: str = "") -> str:
    """
    Prompts user to choose a product from a list of options.
    
    Args:
        options_list (list[str]): List of product options.
        data_map (dict[str, str]): Dictionary mapping user input to product names.
        prompt_text (str, optional): Custom prompt text. Defaults to "".
    
    Returns:
        str: The chosen product name.
    """
    if prompt_text != "":
        user_input = input(prompt_text).strip()
    else:
        user_input = input(f"Choose a vehicle {options_list}: \n>> ").strip()
    # take user input string and make it lower case then call the lowercase dict to invoke the correct KEY
    key = data_map.get(user_input.lower())
    if key:
        return key  # Return the correctly cased product name
    return user_input


def is_exit_key(input: str) -> bool:
    """
    Checks if input is exit key.
    
    Args:
        input (str): User input string.
    
    Returns:
        bool: True if input is exit key, False otherwise.
    """
    return input == "done"


def get_build_quantity(product_name: str) -> int:
    """
    Prompts user to input quantity of a product to build.
    
    Args:
        product_name (str): Name of the product.
    
    Returns:
        int: Quantity of the product to build.
    """
    try:
        user_input = input(f"How many {product_name} do you want to build?\n>> ").strip()
        if user_input.lower() == "exit":
            raise SystemExit(0)
        quantity = int(user_input)
        return quantity
    except ValueError:
        print("Not a number, type a number.\n")
        return get_build_quantity(product_name)


def is_user_input_in_map(x: str, data_map: dict[str, Any]) -> bool:
    """
    Checks if user input is in data map.
    
    Args:
        x (str): User input string.
        data_map (dict[str, Any]): Dictionary mapping user input to product names.
    
    Returns:
        bool: True if user input is in data map, False otherwise.
    """
    return x in data_map


def calculate_total_resources(user_selections: list[tuple[str, int]], Products: dict[str, Any]) -> dict[str, float]:
    """
    Calculates total resources needed for building products.
    
    Args:
        user_selections (list[tuple[str, int]]): List of tuples containing product name and quantity.
        Products (dict[str, Any]): Dictionary of products with their attributes.
    
    Returns:
        dict[str, float]: Dictionary of total resources needed.
    """
    total: dict[str, float] = dict() 
    # iterate over products picked by user and get their true key
    for product_name, amount in user_selections:
        product_picked = Products[product_name]
        if hasattr(product_picked, 'total_basic_resources'):
            try:
                # throws the return of the method in resources
                resources: dict[str, float] = product_picked.total_basic_resources()
            except RecursionError as e:
                print(f"Error calculating resources for '{product_name}': {e}\n")
                continue
            # multiplies each value by set amount in users_map value
            resources = {k: v * amount for k, v in resources.items()}
            print(f"{product_name} x{amount}: { {k: int(v) for k, v in resources.items()} }\n")
            sum_resources_from_each_product(resources, total)
    return total


def sum_resources_from_each_product(data_map: dict[str, float], ref: dict[str, float]) -> None:
    """
    Sums resources from each product in data_map into ref dictionary.
    
    Args:
        data_map (dict[str, float]): Dictionary of resources from each product.
        ref (dict[str, float]): Dictionary to store summed resources.
    """
    for k, v in data_map.items():
        ref[k] = ref.get(k, 0.0) + v



def get_materials(user_selections: list[tuple[str, int]], Products: dict[str, Any]) -> dict[str, float]:
    """
    Calculates total materials needed for building products.
    
    Args:
        user_selections (list[tuple[str, int]]): List of tuples containing product name and quantity.
        Products (dict[str, Any]): Dictionary of products with their attributes.
    
    Returns:
        dict[str, float]: Dictionary of total materials needed.
    """
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
