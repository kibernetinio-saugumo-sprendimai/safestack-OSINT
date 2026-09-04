import unittest

from core_control.registry import build_default_registry
from cli.ss_osint import build_parser


class SmokeTest(unittest.TestCase):
    def test_cli_parser(self):
        parser = build_parser()
        args = parser.parse_args(["run", "all", "example.com", "--policy", "policy.json"])
        self.assertEqual(args.command, "run")
        self.assertEqual(args.module, "all")
        self.assertEqual(args.target, "example.com")

    def test_default_registry_modules(self):
        registry = build_default_registry()
        module_names = set(registry.list_modules().keys())
        self.assertIn("dns.live", module_names)
        self.assertIn("whois.rdap", module_names)
        self.assertIn("tls.info", module_names)

    def test_imports(self):
        # Test that all core imports work without errors
        try:
            from core_control.context import Context
            from core_control.policy import Policy
            from core_control.result import Result
            from core_control.exceptions import ModuleExecutionError
        except ImportError as e:
            self.fail(f"Import failed: {e}")

    def test_policy_is_default_deny(self):
        from core_control.context import Context
        from core_control.policy import Policy

        policy = Policy(
            allowed_modes=["network"],
            module_modes={"dns.live": ["network"]},
            allowed_modules=["dns.live"],
            denied_modules=[],
            allowed_targets=["example.com"],
        )
        Context(target="example.com", mode="network", policy=policy)
        with self.assertRaises(ValueError):
            Context(target="unauthorized.example", mode="network", policy=policy)

    def test_dns_failure_does_not_fabricate_address(self):
        from modules.passive_dns.module import PassiveDNSModule

        result = PassiveDNSModule()._error("example.com", "timeout")
        self.assertEqual(result["records"], [])
        self.assertEqual(result["error"], "dns_failed")


if __name__ == "__main__":
    unittest.main()
