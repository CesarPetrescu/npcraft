"""Static contracts complement, but never replace, real Minecraft assertions."""
import json
from pathlib import Path
import unittest
from tools.agent_tests import AGENT_TESTS

ROOT = Path(__file__).resolve().parents[1]
F = ROOT / 'datapack/data/npcraft/function'

class AgentContracts(unittest.TestCase):
    def test_backpack_has_36_slots_including_hotbar(self):
        text=(F/'agent/init.mcfunction').read_text()
        self.assertIn('version:1,slots:[' + ','.join('{}' for _ in range(36)) + ']', text)

    def test_staging_does_not_mutate_authoritative_inventory(self):
        for name in ('insert', 'merge', 'merge_slot', 'empty', 'empty_slot', 'remove', 'remove_loop', 'remove_slot'):
            text=(F/f'inventory/{name}.mcfunction').read_text()
            self.assertNotIn('data modify entity', text, name)

    def test_transfer_checks_capacity_before_clearing_hand(self):
        text=(F/'inventory/give.mcfunction').read_text()
        self.assertLess(text.index('unless score #inv_ok'),text.index('weapon.mainhand with minecraft:air'))
        self.assertLess(text.index('weapon.mainhand with minecraft:air'),text.index('inventory/commit'))

    def test_mine_commit_revalidates_before_mutation(self):
        text=(F/'actions/mine_commit.mcfunction').read_text()
        point=text.index('run setblock')
        for check in ('work/in_bounds','unless loaded','work/sight','need_plain_pickaxe','inventory/insert','unless score #inv_ok'):
            self.assertLess(text.index(check), point)
        self.assertGreater(text.index('inventory/commit'), point)

    def test_vertical_clearance_not_just_landing(self):
        text=(F/'nav/step_safe.mcfunction').read_text()
        self.assertIn('matches -2..1',text)
        self.assertIn('unless block ~ ~3 ~',text)
        self.assertIn('unless block ~ ~2 ~',text)
        self.assertIn('unless score #tx np.tmp matches 1',text)

    def test_stop_records_cancellation(self):
        text=(F/'commands/owned.mcfunction').read_text()
        self.assertIn('state:"cancelled",reason:"owner_stop"',text)
        self.assertIn('data remove entity @s data.target',text)

    def test_action_dispatch_is_closed(self):
        text=(F/'actions/run.mcfunction').read_text()
        self.assertNotIn('$(',text)
        self.assertIn('unsupported_action',text)

    def test_new_dialog_only_sends_triggers(self):
        dialog=json.loads((ROOT/'datapack/data/npcraft/dialog/agent.json').read_text())
        for button in dialog['actions']:
            self.assertRegex(button['action']['command'],r'^trigger npcraft set \d+$')

    def test_end_to_end_and_fault_regressions_exist(self):
        names={test.__name__ for test in AGENT_TESTS}
        self.assertGreaterEqual(len(names),18)
        self.assertTrue({'test_agent_goal_end_to_end','test_agent_recipe_atomicity',
                         'test_agent_inventory_capacity_rollback','test_agent_backpack_persists',
                         'test_agent_head_sweep_revalidation'}.issubset(names))
