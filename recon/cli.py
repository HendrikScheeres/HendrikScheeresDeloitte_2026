"""recon run --date YYYY-MM-DD"""
from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

from .findings import Finding, build_findings
from .readers import load_day

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def format_amount(amount_cents: int) -> str:
    sign = "-" if amount_cents < 0 else ""
    whole, cents = divmod(abs(amount_cents), 100)
    return f"€{sign}{whole}.{cents:02d}"


def print_finding(finding: Finding) -> None:
    print(f"  {finding['type']} ({finding['key']})")
    if "reason" in finding:
        print(f"    Review: {finding['reason']}")
    for record in finding["records"]:
        amount = format_amount(record["amount_cents"])
        print(
            f"    {record['source']} | ref={record['ref']}"
            f" | id={record['id'] or 'no ID'} | amount={amount}"
            f" | time={record['timestamp']} | merchant={record['merchant']}"
        )


def print_report(date: str, findings: list[Finding]) -> None:
    print(f"Reconciliation — {date}")
    counts = Counter(finding["type"] for finding in findings)
    print(f"\n{len(findings)} findings")
    for finding_type in sorted(counts):
        print(f"  {finding_type}: {counts[finding_type]}")

    if findings:
        print("\nDetails:")
        for finding in findings:
            print_finding(finding)
    else:
        print("No discrepancies found.")


def run(date: str, data_dir: Path) -> int:
    provider, ledger = load_day(data_dir, date)
    findings = build_findings(provider, ledger)
    print_report(date, findings)
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
