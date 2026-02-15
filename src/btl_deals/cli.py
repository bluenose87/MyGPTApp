from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import process_deals


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze BTL deals and export ranked spreadsheet")
    parser.add_argument("input_csv", type=Path, help="Path to input listings CSV")
    parser.add_argument("output_excel", type=Path, help="Path to output Excel file (.xlsx)")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    ranked = process_deals(args.input_csv, args.output_excel)
    print(f"Processed {len(ranked)} deals")
    print(f"Top deal: {ranked.loc[0, 'address']} (score={ranked.loc[0, 'deal_score']:.3f})")
    print(f"Saved workbook to: {args.output_excel}")


if __name__ == "__main__":
    main()
