# Policy System

The SafeStack OSINT framework uses a policy-driven execution model. Policies define the boundaries of what is allowed during an OSINT operation, ensuring compliance and accountability.

## Policy Schema

Policies are defined in JSON files. Below are the available fields:

| Field | Type | Description |
|-------|------|-------------|
| `allowed_modes` | `List[str]` | Global explicit allow-list of execution modes; bundled network modules use `network`. |
| `module_modes` | `Dict[str, List[str]]` | Per-module mode restrictions. Overrides global settings for specific modules. |
| `allowed_modules`| `List[str]` | Explicit allow-list of modules. If defined, only these modules can run. |
| `denied_modules` | `List[str]` | Explicit deny-list. These modules will NEVER run. |
| `allowed_targets` | `List[str]` | Required allow-list of exact domains, wildcard subdomains or IP networks. |
| `notes` | `str` | Metadata for audit purposes (e.g., reason for the policy). |

## Example `policy.json`

```json
{
  "allowed_modes": ["network"],
  "allowed_modules": ["dns.live", "whois.rdap", "tls.info"],
  "denied_modules": [],
  "module_modes": {
    "dns.live": ["network"],
    "whois.rdap": ["network"],
    "tls.info": ["network"]
  },
  "allowed_targets": ["example.com", "*.example.com"],
  "notes": "Explicitly authorized targets only."
}
```

## Enforcement

Policies are mandatory. Missing or empty allow-lists fail closed. The CLI loads them using `--policy`:

```bash
ss-osint run all example.com --policy policy.json
```

If a module execution violates the policy, the framework will raise a `PolicyViolationError` and log the event in the audit logs.
