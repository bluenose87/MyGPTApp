from pathlib import Path

import pandas as pd
import pytest

from btl_deals.analyzer import (
    _monthly_interest_rate,
    calculate_metrics,
    export_ranked_to_excel,
    process_deals,
    rank_deals,
    read_listings,
    score_deals,
)


def sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "listing_id": "A1",
                "address": "10 High Street",
                "purchase_price": 150000,
                "monthly_rent": 950,
                "deposit_percent": 25,
                "interest_rate_percent": 5.0,
                "monthly_costs": 180,
            },
            {
                "listing_id": "B2",
                "address": "20 Market Road",
                "purchase_price": 175000,
                "monthly_rent": 1150,
                "deposit_percent": 25,
                "interest_rate_percent": 5.5,
                "monthly_costs": 220,
            },
        ]
    )


def test_read_listings(tmp_path: Path) -> None:
    csv_path = tmp_path / "listings.csv"
    sample_df().to_csv(csv_path, index=False)

    df = read_listings(csv_path)

    assert len(df) == 2
    assert "address" in df.columns


def test_read_listings_missing_columns(tmp_path: Path) -> None:
    csv_path = tmp_path / "invalid.csv"
    pd.DataFrame([{"listing_id": "X1"}]).to_csv(csv_path, index=False)

    with pytest.raises(ValueError):
        read_listings(csv_path)


def test_monthly_interest_rate() -> None:
    rates = pd.Series([6.0])
    monthly = _monthly_interest_rate(rates)
    assert monthly.iloc[0] == pytest.approx(0.005)


def test_calculate_metrics() -> None:
    result = calculate_metrics(sample_df())

    first = result.iloc[0]
    assert first["deposit_amount"] == pytest.approx(37500)
    assert first["loan_amount"] == pytest.approx(112500)
    assert first["monthly_cashflow"] == pytest.approx(301.25)


def test_score_deals() -> None:
    scored = score_deals(calculate_metrics(sample_df()))
    assert "deal_score" in scored.columns
    assert scored["deal_score"].between(0, 1).all()


def test_rank_deals() -> None:
    ranked = rank_deals(score_deals(calculate_metrics(sample_df())))
    assert ranked.iloc[0]["rank"] == 1
    assert ranked["deal_score"].is_monotonic_decreasing


def test_export_ranked_to_excel(tmp_path: Path) -> None:
    ranked = rank_deals(score_deals(calculate_metrics(sample_df())))
    output = tmp_path / "ranked_deals.xlsx"

    written = export_ranked_to_excel(ranked, output)

    assert written.exists()
    reloaded = pd.read_excel(written)
    assert len(reloaded) == len(ranked)


def test_process_deals(tmp_path: Path) -> None:
    input_csv = tmp_path / "input.csv"
    output_excel = tmp_path / "output.xlsx"
    sample_df().to_csv(input_csv, index=False)

    ranked = process_deals(input_csv, output_excel)

    assert output_excel.exists()
    assert len(ranked) == 2
    assert ranked.iloc[0]["rank"] == 1
