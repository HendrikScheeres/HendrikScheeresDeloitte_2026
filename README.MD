# Daily transaction reconciliation

A small Python command-line tool that compares daily payment-provider and internal-ledger exports and reports discrepancies for review.
Performed assignment as part of an interview process for role of Software Engineer at Deloitte.

## Requirements

- Python 3.11 or newer
- No third-party packages

## Run

From the repository root:

```bash
python3 -m recon run --date 2026-03-01
```

The date selects these input files in `data/`:

```text
data/provider-2026-03-01.jsonl
data/ledger-2026-03-01.csv
```

To read exports from another directory, pass `--data-dir`:

```bash
python3 -m recon run --date 2026-03-01 --data-dir /path/to/exports
```

Both files for the requested date must exist. The command prints a summary and transaction details to the terminal.

## What it reports

- Transaction IDs present only in the provider export or only in the ledger export.
- Shared transaction IDs with different amounts.
- Repeated IDs that make individual records ambiguous.
- Records without a transaction ID, listed individually for human review.

Amounts are compared as integer euro cents. Provider timestamps are read as UTC; ledger timestamps are interpreted in `Europe/Amsterdam` and converted to UTC. Merchant names are included in the report but are not compared because the two systems use different descriptions.

## Current scope and limitations

The current command analyzes one date at a time. It does not yet persist findings or report which discrepancies are new, changed, or resolved between runs. Records without IDs are surfaced but are not automatically paired; the available fields and business rules are not enough to make every such match safely.

## Tests

Run the normalization tests from the repository root:

```bash
python3 -m unittest
```

The tests compare the normalization of sample provider and ledger records with the worked examples in `docs/normalize_golden.json`.

## Project files

- `recon/readers.py` reads the JSONL and CSV exports.
- `recon/normalize.py` converts raw rows to a shared transaction shape.
- `recon/findings.py` classifies discrepancies for a single day.
- `recon/cli.py` formats and prints the report.
- `docs/DATA_SPEC.md` documents input fields and normalization rules.
- `LOG.MD` records implementation notes, observations, and open questions.