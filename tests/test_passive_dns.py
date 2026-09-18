import unittest

from modules.passive_dns.module import PassiveDNSModule


class PassiveDNSFallbackTest(unittest.TestCase):
    def test_fallback_never_fabricates_records(self):
        result = PassiveDNSModule()._fallback("example.com", "resolver unavailable")

        self.assertEqual(result["records"], [])
        self.assertEqual(result["source"], "stub")
        self.assertEqual(result["error"], "DNS_UNAVAILABLE")


if __name__ == "__main__":
    unittest.main()
