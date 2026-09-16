"""Offline regression contracts; runtime/GUI assertions live in separate suites."""
from pathlib import Path
import unittest
from tools.build import ROOT

F = ROOT/'datapack/data/npcraft/function'
class V03Contracts(unittest.TestCase):
    def text(self, path): return (F/path).read_text()
    def test_consent_withdrawal_precedes_proximity_and_dimension(self):
        text=self.text('commands/dispatch.mcfunction')
        self.assertLess(text.index('matches 42'),text.index('unless dimension'))
        self.assertLess(text.index('matches 42'),text.index('npcraft.allowed'))
    def test_consent_epochs_are_authoritative(self):
        text=self.text('rival/access_check.mcfunction')+self.text('rival/consent_check.mcfunction')
        self.assertIn('consents',text);self.assertIn('token',text);self.assertIn('acl',text)
        self.assertIn('consents[{id:',self.text('rival/revoke_consent.mcfunction'))
    def test_goal_completion_uses_supported_tool(self):
        text=self.text('agent/observe.mcfunction')
        self.assertIn('#pick_best',text)
        self.assertNotIn('inventory/count {kind:"minecraft:stone_pickaxe"}',text)
    def test_descriptive_components_do_not_mutate_real_tool(self):
        text=self.text('inventory/pick_check.mcfunction')
        for field in ('custom_name','lore','custom_data'):
            self.assertIn('compare.components."minecraft:'+field+'"',text)
        self.assertNotIn('data remove entity',text)
    def test_routes_are_per_controller(self):
        text=self.text('nav/save_route.mcfunction')
        self.assertIn('entity @s data.navigation.steps',text)
        self.assertIn('function npcraft:nav/move',self.text('nav/advance.mcfunction'))
        self.assertIn('step_safe',self.text('nav/move_macro.mcfunction'))
    def test_native_furnace_transfer_order(self):
        for name in ('feed','fuel','collect'):
            text=self.text('stations/'+name+'.mcfunction')
            self.assertLess(text.index('item replace block'),text.index('inventory/commit'))
        self.assertIn('furnace_missing_or_replaced',self.text('stations/operate.mcfunction'))
    def test_navigation_does_not_edit_terrain(self):
        for path in (F/'nav').glob('*.mcfunction'):
            text='\n'.join(x for x in path.read_text().splitlines() if not x.startswith('#'))
            for word in ('setblock','fill ','clone '): self.assertNotIn(word,text,str(path))
    def test_death_tombstone_precedes_inventory_drops(self):
        text=self.text('survival/died.mcfunction')
        self.assertLess(text.index('dead set value 1b'),text.index('survival/drop_all'))
        self.assertIn('npcraft_visual',self.text('runtime/tick.mcfunction'))
    def test_release_reuses_full_ci(self):
        ci=(ROOT/'.github/workflows/ci.yml').read_text()
        self.assertIn('needs: [quality, vanilla, visual, soak]',ci)
        self.assertIn('uses: ./.github/workflows/client-playtest.yml',ci)
        self.assertIn('uses: ./.github/workflows/ci.yml',(ROOT/'.github/workflows/release.yml').read_text())
    def test_maintained_test_workflows_have_no_write_permission(self):
        for name in ('ci.yml','client-playtest.yml'):
            text=(ROOT/'.github/workflows'/name).read_text()
            self.assertNotIn('contents: write',text)
            self.assertNotIn('pull_request_target',text)
