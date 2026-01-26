# FacilityCalc

A resource calculator for Foxhole facility production. Calculate the total basic resources (Salvage, Coal, Sulfur, Rare Metals) needed to build vehicles and structures.

## Usage

Requires Python 3.9+

```bash
python main.py
```

1. Choose whether to display facility material costs (type `1`) or skip
2. Select products by name (case-insensitive)
3. Enter the quantity for each product
4. Type `done` to calculate totals

## Available Products

Outlaw, Chieftain, Thornfall, ATHT, Skycaller, RAC, King Jester, Flame BT, MG BT, SPG, RSC, SC, IC, UF, Sub, Frigate, Bluefin, Longhook, Bowhead

## Development

### Setup

```bash
poetry install
```

### Dependencies

- **pytest** - Unit testing
- **mypy** - Static type checking

### Running Tests

```bash
poetry run pytest
```

### Type Checking

```bash
poetry run mypy .
```

## Known Limitations

- **Product selection overwrites previous entries**: Selecting the same product twice replaces the first quantity instead of adding to it. For example, selecting `SPG: 1`, then `Chieftain: 3`, then `SPG: 3` results in only 3 SPGs being calculated, not 4.
