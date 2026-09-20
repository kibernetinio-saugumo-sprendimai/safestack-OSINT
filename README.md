# SafeStack OSINT

**SafeStack OSINT** is a modular, policy-controlled OSINT framework for
controlled, explainable and cryptographically verifiable information gathering.

The project prioritizes responsibility, auditability and technical honesty over
collection volume.

> **Your data. Your rules. Your trust chain.**

## Features

- Modular OSINT architecture (DNS, WHOIS/RDAP and TLS)
- Centralized **Policy** system defining what is allowed, when and how
- `run all` execution mode
- Deterministic confidence scoring
- Risk flags and human-readable hints
- JSON reports
- Report signing with minisign
- Offline report verification

## Installation

### 1. Virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

If editable installation fails because dependencies are missing:

```bash
pip install dnspython requests
```

The `minisign` tool is required to sign reports. Download it from
https://jedisct1.github.io/minisign/.

## Usage

Run one module:

```bash
ss-osint run dns.passive example.com
```

Run all modules:

```bash
ss-osint run all example.com
```

Use a policy:

```bash
ss-osint run all example.com --policy policy.json
```

Run through Python:

```bash
python -m cli.ss_osint run all example.com
```

On Windows, use `run_osint.bat` or PowerShell:

```powershell
.\run_osint.ps1 run all example.com
```

## Reports and verification

```bash
ss-osint run all example.com --policy policy.json --report report.json
```

The result includes `report.json` and `report.json.sig` (or `.minisig`). Verify
offline:

```bash
minisign -V -m report.json -p safestack.pub
```

A successful verification confirms that the report was not modified and that it
was signed by the expected source. It does not prove that the underlying
information is complete or correct.

## Risk and confidence model

Confidence is calculated only from successful modules and is deterministic.
Example risk flags include `no_tls`, `multiple_ips` and `whois_private`.

Human-readable hints can include:

- “TLS is present and active.”
- “Multiple IP addresses detected — likely CDN usage.”
- “WHOIS registrar information is present and identifiable.”

## Project structure

```text
.
├── adapters/          # Framework-to-module adapters
├── cli/               # CLI entry points
├── core_control/      # Execution core, reporting, risk and policy
├── docs/              # Documentation
├── modules/           # OSINT modules
├── tests/              # Smoke and integration tests
├── run_osint.bat      # Windows launcher
├── run_osint.ps1      # PowerShell launcher
├── pyproject.toml
├── README.md
├── LICENSE
├── CHANGELOG.md
├── safestack.key      # Offline private signing key; never publish it
└── safestack.pub      # Public verification key
```

## Documentation

See the `docs/` directory:

- [Policy system](docs/POLICY.md) — configure `policy.json`.
- [Audit and traceability](docs/AUDIT.md) — logging and signing reports and configuration.
- [Module development](docs/MODULES.md) — add a new OSINT module.
- [Configuration](docs/CONFIGURATION.md) — prepare the environment.
- [Reproducibility](docs/REPRODUCIBILITY.md) — repeat investigations consistently.

## Versioning notice

Earlier tags (`v0.2.0`, `v0.3.0`, `v0.4.0` and `v1.0.0`) were created during
rapid, non-linear development and do not represent stable or coherent releases.
They are preserved for historical reference. Versioning discipline and release
guarantees start from `v1.5.0` onward.
