import unittest

from core_control.registry import build_default_registry
from cli.ss_osint import build_parser


class SmokeTest(unittest.TestCase):
    def test_cli_parser(self):
        parser = build_parser()
        args = parser.parse_args(["run", "all", "example.com"])
        self.assertEqual(args.command, "run")
        self.assertEqual(args.module, "all")
        self.assertEqual(args.target, "example.com")

    def test_default_registry_modules(self):
        registry = build_default_registry()
        module_names = set(registry.list_modules().keys())
        self.assertIn("dns.passive", module_names)
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


if __name__ == "__main__":
    unittest.main()
