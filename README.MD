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

The command saves a rolling list of open findings in `recon-state.json` in the data directory. On each run, it checks the saved findings against that date's exports, keeps findings it cannot confirm as resolved, and adds that date's findings. A finding with an ID is considered resolved only when the opposite-side record appears exactly once with the same amount. Amount mismatches are considered resolved when the ID appears exactly once on both sides with equal amounts.

The state currently has these limits:

- The report shows exceptions for the requested date, not which findings are new, changed, or resolved compared with the saved state.
- Resolution is checked using only the current date's exports -> a finding is not cleared merely because its ID is absent from both files for that date.
- Findings without an ID and findings for repeated IDs are never considered resolved automatically, so they remain open in state.
- Re-running the most recently processed date leaves state unchanged. The state stores only `last_processed_date`, so running an older date after a newer one is not rejected and can replace the rolling state with results based on that older date.

Records without IDs are listed for human review and are not automatically paired; the available fields and business rules are not enough to make every such match safely.

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
