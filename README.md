# Star Citizen Fleet Value Report

A simple Python utility for analyzing your Star Citizen fleet value using a CSV export from CCU Game.

The script calculates:

- Total MSRP value
- Total melt / pledge value
- Value gained through CCUs
- Package-by-package breakdowns
- Effective fleet discount

Includes ANSI-colored terminal output for readability.

---

# Sample Output

```text
================================================================================
STAR CITIZEN FLEET VALUE REPORT
================================================================================

Unique Pledges / Packages: 14
Contained Ship Rows:       32

Total MSRP:                $9,435.00
Total Pledge / Melt Basis: $7,592.30
Value Over Melt:           +$1,842.70
Effective Discount:        19.53% below MSRP

================================================================================
PACKAGE BREAKDOWN
================================================================================

[UEE Exploration 2948 Pack]

Package Melt Value: $2,115.00
Package MSRP Value: $3,195.00
Value Over Melt:    +$1,080.00
Discount:           33.80%
```

---

# Installation

## Requirements

- Python 3.9+
- No external dependencies

## Export Your Fleet

1. Open CCU Game (https://ccugame.app/your-items/ships)
2. Sync your hangar
3. Export your ships CSV

Example:

```text
ships_2026-05-23.csv
```

## Run

```bash
python main.py ships_2026-05-23.csv
```