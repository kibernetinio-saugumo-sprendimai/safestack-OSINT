# Reproducibility

Ensuring that OSINT scans are reproducible is critical for forensic analysis and evidence gathering.

## 🕒 Determinism

SafeStack OSINT strives for determinism where possible:
- **Confidence Scoring**: Calculated using the same average algorithm across all scans.
- **Timestamping**: All events use UTC ISO 8601 timestamps.
- **Report Structure**: Canonical JSON sorting is applied to reports.

## 🛠️ Environment Consistency

To reproduce a scan exactly, the following must match:
- **Version**: Check `CHANGELOG.md` or git tags for the specific release used.
- **Policy**: Use the same `policy.json` file.
- **Dependencies**: Ensure the same versions of `dnspython`, `requests`, and `minisign` are installed.

## 📋 Scan Context

Each report includes a `meta` section with the `target_confidence` and `generated_at` timestamp. Always preserve the `.minisig` file alongside the report to maintain the chain of trust.

### Scanner Policies
- **TLS Version**: The scanner enforces a minimum TLS version (default: TLS 1.2) during certificate retrieval. This can affect results if the target only supports older versions.
- **Timeouts**: Default timeouts (3-5s) are used for all modules to ensure consistent execution times.
