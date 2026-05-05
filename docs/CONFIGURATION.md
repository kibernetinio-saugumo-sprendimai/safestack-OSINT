# Configuration & Setup

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -e .
   ```

2. **Verify Environment**:
   Run the included PowerShell script to check for system dependencies like `minisign`:
   ```powershell
   .\setup_env.ps1
   ```

## ⚙️ Configuration

### Environment Variables
While most configuration is handled via `policy.json`, some modules may require environment variables for API keys (if applicable).

### Cryptographic Setup
The framework uses a public key (`safestack.pub`) for report verification. 
- To generate a new key pair:
  ```bash
  minisign -G
  ```
- Replace `safestack.pub` with your new public key.

### Logging
Audit logs are stored in `logs/audit/`. Ensure the application has write permissions to this directory. You can customize the log directory in `core_control/runner.py`.

## 🧪 Testing
Run the test suite to ensure everything is configured correctly:
```bash
pytest
```
