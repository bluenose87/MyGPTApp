# BTL Property Deal Spreadsheet Analyzer

This project builds a **Python 3.11+** workflow to:
1. Read property listings from CSV.
2. Calculate rental yield and cashflow metrics.
3. Score and rank deals.
4. Export ranked results to an Excel spreadsheet (`.xlsx`) using `openpyxl`.

It is written with **cross-platform paths** (`pathlib`), so it runs on Windows, macOS, and Linux.

## 1) Files / modules created

```text
src/btl_deals/
  __init__.py        # Public exports
  analyzer.py        # Core business logic and pipeline
  cli.py             # Command-line entry point
tests/
  test_analyzer.py   # Tests for every function
examples/
  listings_sample.csv
  ranked_preview.csv # Example ranked output (CSV preview)
pyproject.toml       # Python/project/test dependencies
```

## 2) Code overview

### `analyzer.py` functions
- `read_listings(csv_path)`: reads and validates CSV columns.
- `_monthly_interest_rate(annual_percent)`: helper for monthly mortgage interest.
- `calculate_metrics(df)`: computes deposit, loan, gross yield, cashflow, and cash-on-cash return.
- `score_deals(df)`: normalizes metrics and applies weighted scoring.
- `rank_deals(df)`: sorts by score and assigns rank.
- `export_ranked_to_excel(df, output_path)`: writes `.xlsx` with `openpyxl` engine.
- `process_deals(input_csv, output_excel)`: end-to-end pipeline.

### `cli.py` usage
```bash
python -m btl_deals.cli examples/listings_sample.csv examples/ranked_deals.xlsx
```

## 3) Input and output examples

### Example input (`examples/listings_sample.csv`)
```csv
listing_id,address,purchase_price,monthly_rent,deposit_percent,interest_rate_percent,monthly_costs
P001,10 High Street,150000,950,25,5.0,180
P002,20 Market Road,175000,1150,25,5.5,220
P003,1 Station Avenue,140000,1000,20,5.2,160
```

### Example ranked preview (`examples/ranked_preview.csv`)
```csv
rank,listing_id,address,gross_yield_percent,monthly_cashflow,cash_on_cash_return_percent,deal_score
1,P003,1 Station Avenue,8.571428571428571,354.6666666666665,15.199999999999994,1.0
2,P002,20 Market Road,7.885714285714286,328.4375,9.008571428571429,0.31049256676149484
3,P001,10 High Street,7.6,301.25,9.64,0.020396862021227535
```

## 4) How to run (Windows-friendly)

### PowerShell
```powershell
# From project root
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e .

# Run analyzer
python -m btl_deals.cli .\examples\listings_sample.csv .\examples\ranked_deals.xlsx
```

### Command Prompt (cmd.exe)
```bat
py -3.11 -m venv .venv
.\.venv\Scripts\activate.bat
python -m pip install -U pip
python -m pip install -e .
python -m btl_deals.cli .\examples\listings_sample.csv .\examples\ranked_deals.xlsx
```

## 5) Run tests

```bash
python -m pip install -e .[test]
pytest
```

`tests/test_analyzer.py` includes tests for every function in `analyzer.py`.
