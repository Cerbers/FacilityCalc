I will perform the following steps to ensure code quality, type safety, and cleanup:

### 1. Cleanup
I will safely delete `window_main.py` as no references were found in the codebase.
*   **Action**: Delete `c:\Users\Krzysztof\Desktop\foxholelogi\FacilityCalc\window_main.py`.

### 2. Type Safety (`mypy --strict`)
I will refactor `functions.py` and other relevant files to meet `mypy --strict` standards.
*   **Refactor `functions.py`**:
    *   Add proper type hints (e.g., `Dict[str, float]`, `List[str]`).
    *   Rename shadowed variables `list` -> `options_list` and `map` -> `data_map`.
    *   Ensure return types are explicit.
    *   Handle `input` mocking dependency injection if needed for better testing, or keep using `unittest.mock`.
*   **Update `materials.py` and `products.py`**:
    *   Add type annotations to class variables (e.g., `cost: Dict[str, float]`).
    *   Ensure `total_basic_resources` has a return type annotation.

### 3. Unit Testing
I will create a comprehensive test suite for `functions.py`.
*   **Create `tests/test_functions.py`**:
    *   **Test `iterate_and_multiply_keys`**: Verify correct multiplication and accumulation.
    *   **Test `pick_products`**: Mock `input` to simulate user selection (valid, invalid, case-insensitive).
    *   **Test `is_exit_key`**: Verify "done" check.
    *   **Test `user_nums`**: Mock `input` for valid integers and handle `ValueError` (simulating recursion/retry).
    *   **Test `is_user_input_in_map`**: Verify dictionary containment.
    *   **Test `calculate_total_resources`**: Mock product objects with `total_basic_resources` method.
    *   **Test `get_mats`**: Mock product objects with `cost` attribute.

### 4. Verification
*   Run `mypy --strict .` to confirm type compliance.
*   Run `pytest` to verify all tests pass (including the new ones).