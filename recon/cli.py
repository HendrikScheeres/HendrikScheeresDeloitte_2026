"""recon run --date YYYY-MM-DD"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .readers import load_day
from .models import Transaction

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def group_transactions_by_id(
    transactions: list[Transaction],
) :
    """Group records with an ID, retaining all records for duplicate IDs."""
    groups = dict()
    for transaction in transactions:
        if transaction.id:
            groups.setdefault(transaction.id, []).append(transaction)
    return groups


def run(date: str, data_dir: Path) -> int:
    provider, ledger = load_day(data_dir, date)
    print(f"{date}: {len(provider)} provider records, {len(ledger)} ledger rows")

    # Print more information on the data
    provider_without_id = sum(not transaction.id for transaction in provider)
    ledger_without_id = sum(not transaction.id for transaction in ledger)

    provider_ids = {transaction.id for transaction in provider if transaction.id}
    ledger_ids = {transaction.id for transaction in ledger if transaction.id}

    # GENERATE OVERVIEW
    print(f"{date}")
    print(f"{'':28}{'Provider':>10}{'Ledger':>10}")
    print(f"{'Total records':28}{len(provider):>10}{len(ledger):>10}")
    print(f"{'Records without an ID':28}{provider_without_id:>10}{ledger_without_id:>10}")
    print("\n")
    print(f"{'Distinct ids in both:':30}{len(provider_ids & ledger_ids):>8}")

    provider_by_id = group_transactions_by_id(provider)
    ledger_by_id = group_transactions_by_id(ledger)

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="recon")
    sub = parser.add_subparsers(dest="command", required=True)
    p_run = sub.add_parser("run", help="reconcile one day")
    p_run.add_argument("--date", required=True, help="YYYY-MM-DD")
    p_run.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    args = parser.parse_args(argv)
    if args.command == "run":
        return run(args.date, args.data_dir)
    return 2


if __name__ == "__main__":
    sys.exit(main())
