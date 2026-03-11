# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
python main.py                                          # run the app
poetry run pytest                                       # run all tests
poetry run pytest tests/test_main.py -v                # run single test file
poetry run pytest tests/test_main.py::ClassName::method # run single test
poetry run mypy .                                       # type check
```

## Architecture

**Data flow:** `products.json` → `products.py` (dynamic class creation) → `vehicle_groups.py` (faction buckets) → `main.py` (CLI loop) → `functions.py` (calculations) → output.

**`materials.py`** defines all intermediate materials as classes inheriting `Material`. Each has a `cost` dict of basic/intermediate resources and optionally `recipes` (alternative production methods). `materials_map` is the registry used for recursive lookups. `load_recipe_preferences()` reads `recipe_preferences.json` at startup to override default recipes.

**`products.py`** reads `products.json` at import time and dynamically creates subclasses of `Prod` via `type()`, registering them as module globals. Also builds `name_mappings` — a flat dict of all lowercase aliases → canonical product name, used for case-insensitive user input.

**`vehicle_groups.py`** scans the `products` module after load and partitions `Prod` subclasses into `Warden`, `Colonial`, `All` dicts by `faction` attribute.

**Resource calculation** is recursive: `Prod.total_basic_resources()` → `calculate_total_basic_resources()` in `functions.py` → iterates `cost`, recursing into each material's `total_basic_resources()` until hitting a basic resource (Salvage, Coal, Sulfur, Rare Metals, Components).

## Adding Products

Edit `products.json`. Required fields: `faction` (`"warden"`, `"colonial"`, or `"all"`), `names` (list of aliases used for input matching), `cost` (dict using keys from `materials_map` in `materials.py`).

## Adding Materials

Add a class to `materials.py` inheriting `Material` with a `cost` dict, then add it to `materials_map` with its lookup key. That key is what product `cost` dicts reference.

## Testing Rule

After any code or data change, run `poetry run pytest` and confirm all tests pass before considering the task done.

## Code Conventions

- Class attributes for shared data (`cost`, `faction`, `names`); `@classmethod` for methods on class attributes
- Only single-level inheritance from `Material` or `Prod` (no `class X(Coke)`)
- Faction values must be lowercase: `"warden"`, `"colonial"`, `"all"`
- Type hints required on all functions; use built-in `dict`/`list` not `typing.Dict`/`List`
