"""Offline coverage for the exact-version GUI installer's platform selection."""
import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from tools.client_install import allowed, fetch


class ClientInstallTests(unittest.TestCase):
    def test_no_rules_are_allowed(self):
        self.assertTrue(allowed([]))

    def test_only_linux_x64_rules(self):
        self.assertTrue(allowed([{'action': 'allow', 'os': {'name': 'linux', 'arch': 'x86_64'}}]))
        self.assertFalse(allowed([{'action': 'allow', 'os': {'name': 'windows'}}]))
        self.assertFalse(allowed([{'action': 'allow', 'os': {'name': 'linux', 'arch': 'aarch64'}}]))

    def test_later_matching_rule_wins(self):
        self.assertFalse(allowed([{'action': 'allow'}, {'action': 'disallow', 'os': {'name': 'linux'}}]))
        self.assertTrue(allowed([{'action': 'allow'}, {'action': 'disallow', 'os': {'name': 'osx'}}]))

    def test_optional_features_are_not_enabled(self):
        self.assertFalse(allowed([{'action': 'allow', 'features': {'is_demo_user': True}}]))

    def test_insecure_download_refused(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                fetch('http://example.invalid/client.jar', Path(d) / 'client.jar')

    def test_verified_cache_avoids_network(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'asset'
            path.write_bytes(b'example')
            with patch('urllib.request.urlopen', side_effect=AssertionError('Network unexpectedly used')):
                self.assertEqual(fetch('https://example.invalid/asset', path, hashlib.sha1(b'example').hexdigest()), path)


if __name__ == '__main__':
    unittest.main()
