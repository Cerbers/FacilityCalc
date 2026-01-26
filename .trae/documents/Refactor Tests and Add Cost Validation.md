Refactor tests to improve readability and enforce validation for empty cost dictionaries in `Material` and `Prod` classes.

### 1. Enforce Cost Validation in Source Code
- **Modify [materials.py](file:///c:/Users/Krzysztof/Desktop/foxholelogi/FacilityCalc/materials.py)**: Update `Material.total_basic_resources` to raise a `ValueError` with the message "No attributies in cost dictionary in {object name}" if `cost` is empty.
- **Modify [products.py](file:///c:/Users/Krzysztof/Desktop/foxholelogi/FacilityCalc/products.py)**: Update `Prod.total_basic_resources` to raise a `ValueError` with the message "No attributies in cost dictionary in {object name}" if `cost` is empty.

### 2. Refactor Material Tests
- **Update [tests/test_materials.py](file:///c:/Users/Krzysztof/Desktop/foxholelogi/FacilityCalc/tests/test_materials.py)**:
  - Remove inline calculation comments (white noise).
  - Add descriptive docstrings to all test functions.
  - Add a new test case `test_material_empty_cost_exception` to verify that defining a `Material` subclass with an empty cost raises the expected exception.

### 3. Refactor Product Tests
- **Update [tests/test_products.py](file:///c:/Users/Krzysztof/Desktop/foxholelogi/FacilityCalc/tests/test_products.py)**:
  - Remove inline calculation comments.
  - Add descriptive docstrings to all test functions.
  - Add a new test case `test_prod_empty_cost_exception` to verify that defining a `Prod` subclass with an empty cost raises the expected exception.

### 4. Verification
- Run `pytest` to ensure all existing tests pass and the new exception logic is correctly verified.