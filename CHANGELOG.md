# Changelog

All notable changes to SafeStack OSINT are documented in this file.

The format is based on Keep a Changelog principles.

---

## [0.2.0] — 2026-01-17

### Added
- New policy-driven core architecture
- ModuleRegistry with centralized policy enforcement
- Runner orchestration layer
- Context-based execution model
- Canonical Result object
- Adapter-based module system
- CLI (`ss-osint`) entry point
- `dns.passive` adapter
- `whois.rdap` adapter
- `tls.info` adapter (deep-mode restricted)
- Per-module execution mode restrictions (`module_modes`)
- Comprehensive architecture and policy documentation

### Changed
- Execution flow is now strictly controlled via Policy and Registry
- CLI constructs default execution policy
- Deep mode is explicitly required for intrusive modules

### Deprecated
- Previous ad-hoc execution logic (kept for reference)

---

## [0.1.0]
- Initial experimental implementation


## [1.5.0] — 2026-05-05

### Added
- Added signed report export (minisign) using internal Ed25519 signer
- Introduced risk flags and human-readable hints
- Implemented `run all` execution flow
- Added policy enforcement and profiles
- Removed `legacy_core` directory
- Automated code formatting and fixed style issues
