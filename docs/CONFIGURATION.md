# Configuration & Setup

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -e .
   ```

2. **Verify Environment**:
   Run the included PowerShell setup script:
   ```powershell
   .\setup_env.ps1
   ```

## ⚙️ Configuration

### Environment Variables
While most configuration is handled via `policy.json`, some modules may require environment variables for API keys (if applicable).

### Cryptographic Setup
The framework uses a raw Ed25519 public key (`safestack.pub`) for report verification. Private keys must remain outside the repository and are supplied explicitly with `--signing-key`. Use `verify_raw_ed25519.py` for verification; Minisign files are a different format.

### Logging
Audit logs are stored in `logs/audit/`. Ensure the application has write permissions to this directory. You can customize the log directory in `core_control/runner.py`.

## 🧪 Testing
Run the test suite to ensure everything is configured correctly:
```bash
pytest
```
