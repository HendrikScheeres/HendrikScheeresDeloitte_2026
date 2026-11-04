"""recon run --date YYYY-MM-DD"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path
import json

from .findings import Finding, build_findings
from .models import Transaction
from .readers import load_day

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"
FINDING_SECTIONS = (
    ("provider_only", "Only in provider"),
    ("ledger_only", "Only in ledger"),
    ("amount_mismatch", "Different amounts"),
    ("uncertain_match", "Needs manual review"),
    ("without_id", "Records without an ID"),
)


def format_amount(amount_cents: int) -> str:
    sign = "-" if amount_cents < 0 else ""
    whole, cents = divmod(abs(amount_cents), 100)
    return f"€{sign}{whole}.{cents:02d}"


def print_finding(finding: Finding) -> None:
    if finding["transaction_id"]:
        print(f"  ID {finding['transaction_id']}")
    if "reason" in finding:
        print(f"    Review: {finding['reason']}")
    for record in finding["records"]:
        amount = format_amount(record["amount_cents"])
        print(
            f"    {record['source']} | ref={record['ref']}"
            f" | id={record['id'] or 'no ID'} | amount={amount}"
            f" | time={record['timestamp']} | merchant={record['merchant']}"
        )


def print_report(
    date: str,
    provider: list[Transaction],
    ledger: list[Transaction],
    findings: list[Finding],
) -> None:
    print(f"Reconciliation — {date}")
    counts = Counter(finding["type"] for finding in findings)
    provider_ids = {tx.id for tx in provider if tx.id}
    ledger_ids = {tx.id for tx in ledger if tx.id}
    without_id = Counter(
        record["source"]
        for finding in findings
        if finding["type"] == "without_id"
        for record in finding["records"]
    )

    print(f"\nIDs present on both sides: {len(provider_ids & ledger_ids)}")
    print("Needs attention:")
    print(f"  {counts['ledger_only']} IDs only in ledger")
    print(f"  {counts['provider_only']} IDs only in provider")
    print(f"  {counts['amount_mismatch']} IDs with different amounts")
    print(f"  {counts['uncertain_match']} ambiguous ID groups")
    print("Records without an ID:")
    print(f"  {without_id['provider']} in provider")
    print(f"  {without_id['ledger']} in ledger")

    if findings:
        print("\nDetails:")
        for finding_type, label in FINDING_SECTIONS:
            section = [
                finding for finding in findings
                if finding["type"] == finding_type
            ]
            if not section:
                continue
            section.sort(
                key=lambda finding: min(
                    record["timestamp"] for record in finding["records"]
                )
            )
            print(f"\n{label}:")
            for finding in section:
                print_finding(finding)
    else:
        print("No discrepancies found.")

def is_resolved(
    finding: Finding,
    provider: list[Transaction],
    ledger: list[Transaction],
) -> bool:
    transaction_id = finding["transaction_id"]
    if not transaction_id:
        return False

    provider_matches = [tx for tx in provider if tx.id == transaction_id]
    ledger_matches = [tx for tx in ledger if tx.id == transaction_id]

    if finding["type"] == "provider_only":
        old_records = finding["records"]
        return (
            len(old_records) == 1
            and len(ledger_matches) == 1
            and old_records[0]["amount_cents"] == ledger_matches[0].amount_cents
        )

    if finding["type"] == "ledger_only":
        old_records = finding["records"]
        return (
            len(old_records) == 1
            and len(provider_matches) == 1
            and old_records[0]["amount_cents"] == provider_matches[0].amount_cents
        )

    if finding["type"] == "amount_mismatch":
        return (
            len(provider_matches) == 1
            and len(ledger_matches) == 1
            and provider_matches[0].amount_cents == ledger_matches[0].amount_cents
        )

    return False


def run(date: str, data_dir: Path) -> int:
    provider, ledger = load_day(data_dir, date)
    findings = build_findings(provider, ledger)

    # write the state
    state_path = data_dir / "recon-state.json"

    if state_path.exists():
        previous_state = json.loads(state_path.read_text(encoding="utf-8"))
    else:
        previous_state = {"open_findings": []}

    if previous_state.get("last_processed_date") == date:
        print(f"{date} has already been processed; state was not changed.")
        return 0

    still_open = [
    finding
    for finding in previous_state["open_findings"]
    if not is_resolved(finding, provider, ledger)
    ]

    open_findings_by_key = {
        finding["key"]: finding
        for finding in still_open
    }

    for finding in findings:
        open_findings_by_key.setdefault(finding["key"], finding)

    open_findings = list(open_findings_by_key.values())
    state = {
        "last_processed_date": date,
        "open_findings": open_findings,
    }
    state_path.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print_report(date, provider, ledger, findings)
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
