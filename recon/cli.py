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
) -> dict[str, list[Transaction]]:
    """Group records with an ID, retaining all records for duplicate IDs."""
    groups = dict()
    for transaction in transactions:
        if transaction.id:
            groups.setdefault(transaction.id, []).append(transaction)
    return groups


def print_record(tx: Transaction) -> None:
    amount = f"€{tx.amount_cents / 100:.2f}"
    print(
        f"  {tx.source} | ref={tx.ref} | id={tx.id or 'no ID'}"
        f" | amount={amount} | time={tx.timestamp.isoformat()}"
        f" | merchant={tx.merchant}"
    )


def run(date: str, data_dir: Path) -> int:
    provider, ledger = load_day(data_dir, date)
    provider_without_id = sum(not transaction.id for transaction in provider)
    ledger_without_id = sum(not transaction.id for transaction in ledger)
    provider_by_id = group_transactions_by_id(provider)
    ledger_by_id = group_transactions_by_id(ledger)

    shared_ids = provider_by_id.keys() & ledger_by_id.keys()
    provider_only_ids = provider_by_id.keys() - ledger_by_id.keys()
    ledger_only_ids = ledger_by_id.keys() - provider_by_id.keys()

    print(f"Reconciliation — {date}\n")
    print(f"IDs found on both sides: {len(shared_ids)}")
    print("Needs attention:")
    print(f"  {len(ledger_only_ids)} IDs only in ledger")
    print(f"  {len(provider_only_ids)} IDs only in provider")
    print("Records without an ID (not grouped):")
    print(f"  {provider_without_id} in provider")
    print(f"  {ledger_without_id} in ledger")

    print("\nOnly in provider:")
    for transaction_id in sorted(provider_only_ids):
        for tx in provider_by_id[transaction_id]:
            print_record(tx)

    print("\nOnly in ledger:")
    for transaction_id in sorted(ledger_only_ids):
        for tx in ledger_by_id[transaction_id]:
            print_record(tx)

    print("\nProvider records without an ID:")
    for tx in provider:
        if not tx.id:
            print_record(tx)

    print("\nLedger records without an ID:")
    for tx in ledger:
        if not tx.id:
            print_record(tx)

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
