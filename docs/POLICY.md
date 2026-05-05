# Policy System

The SafeStack OSINT framework uses a policy-driven execution model. Policies define the boundaries of what is allowed during an OSINT operation, ensuring compliance and accountability.

## Policy Schema

Policies are defined in JSON files. Below are the available fields:

| Field | Type | Description |
|-------|------|-------------|
| `allowed_modes` | `List[str]` | Global list of allowed execution modes (e.g., `["passive", "active"]`). |
| `module_modes` | `Dict[str, List[str]]` | Per-module mode restrictions. Overrides global settings for specific modules. |
| `allowed_modules`| `List[str]` | Explicit allow-list of modules. If defined, only these modules can run. |
| `denied_modules` | `List[str]` | Explicit deny-list. These modules will NEVER run. |
| `allowed_targets` | `List[str]` | (Optional) List of specific targets (domains/IPs) allowed for scanning. |
| `notes` | `str` | Metadata for audit purposes (e.g., reason for the policy). |

## Example `policy.json`

```json
{
  "allowed_modes": ["passive"],
  "denied_modules": ["dns.bruteforce"],
  "module_modes": {
    "tls.info": ["passive", "deep"]
  },
  "notes": "Strict passive-only policy for external audits."
}
```

## Enforcement

Policies are loaded by the CLI using the `--policy` flag:

```bash
ss-osint run all example.com --policy policy.json
```

If a module execution violates the policy, the framework will raise a `PolicyViolationError` and log the event in the audit logs.
