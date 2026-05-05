import os
from pathlib import Path
from core_control.reporting.signing import Signer

def main():
    # 1. Load the private key
    key_path = Path("safestack.key")
    if not key_path.exists():
        print("[ERROR] safestack.key not found. Please create it first.")
        return

    with open(key_path, "r") as f:
        key_hex = f.read().strip()

    signer = Signer(key_hex)

    # 2. Files to sign
    configs_to_sign = [
        ".gitignore",
        "pyproject.toml",
        "README.md",
        "policy.json.example",
        "policy.json",
        "setup_env.ps1",
        "safestack.pub",
        "LICENSE",
        "Audit_Report.pdf"
    ]

    print(f"--- SafeStack Config Signing ---")
    
    for filename in configs_to_sign:
        file_path = Path(filename)
        if file_path.exists():
            if signer.sign_report(str(file_path)):
                print(f"[SUCCESS] Signed: {filename} -> {filename}.sig")
            else:
                print(f"[FAILED]  Could not sign: {filename}")
        else:
            # Skip if file doesn't exist (e.g. policy.json)
            pass

    print("\nAll available configurations have been signed.")

if __name__ == "__main__":
    main()
