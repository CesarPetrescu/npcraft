"""Structural guards supplement, rather than replace, real-server tests."""
from pathlib import Path
import unittest
from tools.build import ROOT

class ReliabilityContracts(unittest.TestCase):
    def test_acl_writer_uses_explicit_byte(self):
        text=(ROOT/'datapack/data/npcraft/function/rival/acl_write.mcfunction').read_text()
        self.assertIn('allowed:$(allowed)b',text)
    def test_eating_rechecks_live_mortal_body(self):
        text=(ROOT/'datapack/data/npcraft/function/survival/eat.mcfunction').read_text()
        self.assertLess(text.index('enabled:1b,dead:0b'),text.index('inventory/load'))
        self.assertIn('unless entity @e[type=minecraft:mannequin',text)
    def test_soak_uses_normal_survival_initializer(self):
        text=(ROOT/'tools/soak_test.py').read_text()
        self.assertIn('function npcraft:survival/enable',text)
        self.assertIn('tick sprint',text)
        self.assertNotIn('function npcraft:progression/tick',text)
    def test_lifecycle_and_scale_are_gated(self):
        text=(ROOT/'.github/workflows/ci.yml').read_text()
        self.assertIn('tools/reliability_tests.py',text)
        self.assertIn('needs: [quality, vanilla, visual, soak]',text)
