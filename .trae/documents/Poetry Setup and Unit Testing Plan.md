I will perform the following steps to set up your environment, clean up existing tests, create new unit tests, and configure gitignore.

### 1. Environment Setup (Poetry)
I will create a `pyproject.toml` file to define the project and its dependencies (`mypy` and `pytest`).
*   **File**: `pyproject.toml`
*   **Content**: Standard Poetry configuration with `python = "^3.10"`, `mypy`, and `pytest` as development dependencies.

### 2. Clean Up
I will delete the existing test files to clear the slate.
*   **Delete**: `tests/test_main.py`
*   **Delete**: `tests/test_products.py`

### 3. Create Unit Tests
I will create comprehensive unit tests for `materials.py` and `products.py`. I will verify the resource calculations.
*   **Create**: `tests/test_materials.py`
    *   Test basic materials (e.g., `Coke`, `Cmat`) to ensure they return correct basic resources.
    *   Test composite materials (e.g., `Steel`, `PCmat`) to ensure recursive calculation works.
*   **Create**: `tests/test_products.py`
    *   Test product resource calculations (e.g., `Chieftain`, `Spad`) using the materials logic.
    *   **Refactor**: I will make a minor adjustment to imports if necessary to ensure tests run smoothly, but the current structure looks mostly testable. I will ensure `materials_map` is correctly accessed.

### 4. Gitignore Configuration
I will create a `.gitignore` file to exclude unnecessary files.
*   **File**: `.gitignore`
*   **Content**: Ignore `__pycache__`, `*.pyc`, `.venv`, `.pytest_cache`, `.mypy_cache`, and `poetry.lock` (optional, usually kept but I'll check your preference, defaulting to keep, but ignoring venv).

### Verification
After creating the files, I will run the tests using `pytest` to ensure everything is working correctly.