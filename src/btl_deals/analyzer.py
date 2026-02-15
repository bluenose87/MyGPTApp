from __future__ import annotations

from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = {
    "listing_id",
    "address",
    "purchase_price",
    "monthly_rent",
    "deposit_percent",
    "interest_rate_percent",
    "monthly_costs",
}


def read_listings(csv_path: str | Path) -> pd.DataFrame:
    """Read listings from a CSV file and validate required columns."""
    path = Path(csv_path)
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        missing_text = ", ".join(sorted(missing))
        raise ValueError(f"CSV is missing required columns: {missing_text}")
    return df.copy()


def _monthly_interest_rate(annual_percent: pd.Series) -> pd.Series:
    return (annual_percent / 100) / 12


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate core BTL metrics for every listing."""
    data = df.copy()

    data["deposit_amount"] = data["purchase_price"] * (data["deposit_percent"] / 100)
    data["loan_amount"] = data["purchase_price"] - data["deposit_amount"]
    data["gross_yield_percent"] = (data["monthly_rent"] * 12 / data["purchase_price"]) * 100

    monthly_rate = _monthly_interest_rate(data["interest_rate_percent"])
    data["monthly_mortgage_interest"] = data["loan_amount"] * monthly_rate

    data["monthly_cashflow"] = (
        data["monthly_rent"] - data["monthly_mortgage_interest"] - data["monthly_costs"]
    )
    data["annual_cashflow"] = data["monthly_cashflow"] * 12
    data["cash_on_cash_return_percent"] = (data["annual_cashflow"] / data["deposit_amount"]) * 100

    return data


def score_deals(df: pd.DataFrame) -> pd.DataFrame:
    """Score listings using normalized yield and cashflow metrics."""
    data = df.copy()

    score_inputs = {
        "gross_yield_percent": 0.45,
        "monthly_cashflow": 0.35,
        "cash_on_cash_return_percent": 0.20,
    }

    for metric, weight in score_inputs.items():
        metric_min = data[metric].min()
        metric_max = data[metric].max()
        if metric_max == metric_min:
            data[f"{metric}_norm"] = 1.0
        else:
            data[f"{metric}_norm"] = (data[metric] - metric_min) / (metric_max - metric_min)
        data[f"{metric}_weighted"] = data[f"{metric}_norm"] * weight

    weighted_columns = [f"{metric}_weighted" for metric in score_inputs]
    data["deal_score"] = data[weighted_columns].sum(axis=1)
    return data


def rank_deals(df: pd.DataFrame) -> pd.DataFrame:
    """Sort deals by score descending and assign 1-based rank."""
    ranked = df.sort_values(by="deal_score", ascending=False).reset_index(drop=True)
    ranked["rank"] = ranked.index + 1
    return ranked


def export_ranked_to_excel(df: pd.DataFrame, output_path: str | Path) -> Path:
    """Export ranked deals to an Excel workbook (.xlsx)."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(path, index=False, engine="openpyxl")
    return path


def process_deals(input_csv: str | Path, output_excel: str | Path) -> pd.DataFrame:
    """End-to-end pipeline: read -> calculate -> score -> rank -> export."""
    listings = read_listings(input_csv)
    with_metrics = calculate_metrics(listings)
    scored = score_deals(with_metrics)
    ranked = rank_deals(scored)
    export_ranked_to_excel(ranked, output_excel)
    return ranked
