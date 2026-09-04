# Auditing & Accountability

SafeStack OSINT is designed for "Zero-Trust" environments where every action must be verifiable and auditable.

## 🛡️ Audit Logs

The framework maintains persistent, structured logs of all module executions.

- **Location**: `logs/audit/audit_YYYY-MM-DD.jsonl`
- **Format**: JSON Lines (JSONL)

### Log Entry Schema

Each log entry contains:
- `timestamp`: UTC time of execution.
- `target_sha256`: SHA-256 of the normalized target; the raw target is not retained in the audit log.
- `module`: The name of the module.
- `status`: `SUCCESS`, `WARNING` (data issues), or `FAILED` (error).
- `summary`: High-level results (confidence, sources, error details).

## 🔐 Cryptographic Integrity

Reports can be signed using the documented SafeStack raw Ed25519 v1 format. This is not Minisign.

### Sign Scan Results
When running with the `--report` flag, the framework attempts to sign the output:
```bash
ss-osint run all example.com --policy policy.json --report my_report.json --signing-key /secure/offline/private-key.hex
```
This generates `my_report.json` and `my_report.json.sig`.

### Sign Framework Configuration
To ensure the integrity of the framework itself, you can sign all critical configuration files:
```bash
python sign_configs.py --signing-key /secure/offline/private-key.hex README.md policy.json.example
```
This signs `.gitignore`, `pyproject.toml`, `policy.json`, etc.

### Verifying a Report
To verify a report offline using the project's public key:
```bash
python verify_raw_ed25519.py --message my_report.json --signature my_report.json.sig --public-key safestack.pub
```

## 🧠 Confidence Scoring

Each module returns a confidence score (0.0 to 1.0) based on the quality of the data source.
- **1.0**: Highly certain (e.g., direct TLS probe, NXDOMAIN).
- **0.9**: Reliable third-party source.
- **0.0**: The module failed or returned no trustworthy data. The framework never fabricates fallback records.

The `RiskEngine` aggregates these scores to provide a target-level confidence rating.
