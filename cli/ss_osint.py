#!/usr/bin/env python3

import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH before importing project packages.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from core_control.reporting.signing import Signer
from core_control.reporting.json_report import generate_json_report
from core_control.policy import Policy
from core_control.exceptions import ModuleExecutionError
from core_control.registry import build_default_registry
from core_control.runner import Runner
from core_control.context import Context
from core_control.safeio import atomic_write, read_regular
import json
import argparse
import subprocess


# -----------------------------
# Argument parser
# -----------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ss-osint",
        description="SafeStack OSINT Framework CLI"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---- run command ----
    run_parser = subparsers.add_parser(
        "run",
        help="Run OSINT module(s)"
    )

    run_parser.add_argument(
        "module",
        help="Module name or 'all'"
    )

    run_parser.add_argument(
        "target",
        help="Target to investigate (domain, IP, etc.)"
    )

    run_parser.add_argument(
        "--mode",
        default="passive",
        help="Execution mode (default: passive)"
    )

    run_parser.add_argument(
        "--policy",
        help="Path to policy.json"
    )

    run_parser.add_argument(
        "--report",
        help="Write JSON report to file"
    )

    run_parser.add_argument(
        "--format",
        choices=["pretty", "json"],
        default="pretty",
        help="Output format for single-module run"
    )

    return parser


# -----------------------------
# Helpers
# -----------------------------

def load_policy(path: str | None) -> Policy:
    if not path:
        return Policy()

    try:
        with open(path, "r") as f:
            data = json.load(f)
        policy = Policy(**data)
        policy.validate()
        return policy
    except Exception as exc:
        raise RuntimeError(f"Failed to load policy file: {exc}") from exc


def print_pretty(result):
    print(f"\nModule     : {result.module}")
    print(f"Target     : {result.target}")
    print(f"Confidence : {result.confidence}")
    print(f"Sources    : {', '.join(result.sources)}")
    print(f"Timestamp  : {result.timestamp.isoformat()}\n")
    print("Data:")
    print(json.dumps(result.data, indent=2))


# -----------------------------
# Main
# -----------------------------

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        policy = load_policy(args.policy)
    except RuntimeError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    context = Context(
        target=args.target,
        mode=args.mode,
        policy=policy
    )

    registry = build_default_registry()
    runner = Runner(registry)

    # ---- run ALL modules ----
    if args.command == "run" and args.module == "all":
        try:
            bundle = runner.run_all(context)
        except ModuleExecutionError as exc:
            print(f"[ERROR] {exc}", file=sys.stderr)
            return 1

        report_data = generate_json_report(
            target=context.target,
            results=bundle["results"],
            errors=bundle["errors"],
            meta=bundle["meta"]
        )

        if args.report:
            atomic_write(args.report, (json.dumps(report_data, indent=2) + "\n").encode())

            # Try internal signer first if safestack.key exists
            key_path = PROJECT_ROOT / "safestack.key"
            signed_internally = False

            if key_path.exists():
                try:
                    key_hex = read_regular(key_path).decode("ascii").strip()
                    signer = Signer(key_hex)
                    if signer.sign_report(args.report):
                        print(
                            "[INFO] Report signed using internal signer (Ed25519).")
                        signed_internally = True
                except Exception as e:
                    print(
                        f"[WARN] Internal signing failed: {e}", file=sys.stderr)

            if not signed_internally:
                # Fallback to minisign binary
                try:
                    subprocess.run(["minisign", "-v"],
                                   capture_output=True, check=False)
                    subprocess.run(
                        ["minisign", "-S", "-m", args.report],
                        check=True
                    )
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print(
                        "[WARN] Report saved but signing failed: 'minisign' not found or failed.",
                        file=sys.stderr)
        else:
            print(json.dumps(report_data, indent=2))

        return 0

    # ---- run SINGLE module ----
    if args.command == "run":
        try:
            result = runner.run(args.module, context)
        except ModuleExecutionError as exc:
            print(f"[ERROR] {exc}", file=sys.stderr)
            return 1

        if args.format == "json":
            print(json.dumps({
                "module": result.module,
                "target": result.target,
                "confidence": result.confidence,
                "sources": result.sources,
                "timestamp": result.timestamp.isoformat(),
                "data": result.data,
            }, indent=2))
        else:
            print_pretty(result)

        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
