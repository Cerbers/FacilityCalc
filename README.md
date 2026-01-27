# FacilityCalc

A resource calculator for Foxhole facility production. Calculate the total basic resources (Salvage, Coal, Sulfur, Rare Metals) needed to build vehicles and structures.
Main aim is to estimate 'worst case scenario' so the conversion rates are fixed for materials.

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

Warden:
Outlaw, Chieftain, Thornfall, ATHT, Skycaller, RAC, King Jester, Flame BT, MG BT, SPG, RSC, S(torm)C(canon), I(ntelligence)C(enter), U(nderground)F(ortress), Sub, Frigate, Bluefin, Longhook, Bowhead

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
- current calculation is based off worst case scenario (i.e. worst coal to coke conversion rates, PCmats made only using material beams recipe, etc.), at the moment switching between states is not being considerate
