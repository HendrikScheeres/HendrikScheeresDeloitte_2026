"""Build structured discrepancy findings from one day's transactions."""
from __future__ import annotations

from typing import Literal, NotRequired, TypedDict

from .models import Transaction

FindingType = Literal[
    "provider_only",
    "ledger_only",
    "amount_mismatch",
    "without_id",
    "uncertain_match",
]


class FindingRecord(TypedDict):
    source: str
    ref: str
    id: str | None
    amount_cents: int
    timestamp: str
    merchant: str


class Finding(TypedDict):
    key: str
    type: FindingType
    transaction_id: str | None
    records: list[FindingRecord]
    reason: NotRequired[str]


def _record_data(tx: Transaction) -> FindingRecord:
    return {
        "source": tx.source,
        "ref": tx.ref,
        "id": tx.id,
        "amount_cents": tx.amount_cents,
        "timestamp": tx.timestamp.isoformat(),
        "merchant": tx.merchant,
    }


def _finding(
    key: str,
    finding_type: FindingType,
    records: list[Transaction],
    transaction_id: str | None = None,
    reason: str | None = None,
) -> Finding:
    result: Finding = {
        "key": key,
        "type": finding_type,
        "transaction_id": transaction_id,
        "records": [_record_data(tx) for tx in records],
    }
    if reason:
        result["reason"] = reason
    return result


def build_findings(
    provider: list[Transaction], ledger: list[Transaction]
) -> list[Finding]:
    """Classify ID-based discrepancies and retain ID-less records for review."""
    provider_by_id: dict[str, list[Transaction]] = {}
    ledger_by_id: dict[str, list[Transaction]] = {}
    for tx in provider:
        if tx.id:
            provider_by_id.setdefault(tx.id, []).append(tx)
    for tx in ledger:
        if tx.id:
            ledger_by_id.setdefault(tx.id, []).append(tx)

    findings: list[Finding] = []
    all_ids = provider_by_id.keys() | ledger_by_id.keys()
    for transaction_id in sorted(all_ids):
        provider_records = provider_by_id.get(transaction_id, [])
        ledger_records = ledger_by_id.get(transaction_id, [])
        key = f"id:{transaction_id}"

        if not ledger_records:
            findings.append(
                _finding(key, "provider_only", provider_records, transaction_id)
            )
        elif not provider_records:
            findings.append(
                _finding(key, "ledger_only", ledger_records, transaction_id)
            )
        elif len(provider_records) == 1 and len(ledger_records) == 1:
            provider_tx = provider_records[0]
            ledger_tx = ledger_records[0]
            if provider_tx.amount_cents != ledger_tx.amount_cents:
                findings.append(
                    _finding(
                        key,
                        "amount_mismatch",
                        [provider_tx, ledger_tx],
                        transaction_id,
                    )
                )
        else:
            findings.append(
                _finding(
                    key,
                    "uncertain_match",
                    provider_records + ledger_records,
                    transaction_id,
                    reason="The ID occurs multiple times; individual records are ambiguous.",
                )
            )

    for tx in provider + ledger:
        if not tx.id:
            key = f"record:{tx.source}:{tx.ref}"
            findings.append(_finding(key, "without_id", [tx]))

    return sorted(findings, key=lambda item: item["key"])
