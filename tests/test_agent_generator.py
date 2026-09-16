"""Offline generator regressions. Actual command behavior is tested in agent_test.py."""
import tempfile
import unittest
from pathlib import Path
from tools.generate_agent import SLOTS, RECIPES, generate, resources

class AgentGenerationTests(unittest.TestCase):
    def test_deterministic(self):
        self.assertEqual(resources(), resources())

    def test_checked_in_runtime(self):
        self.assertEqual(generate(check=True), [])

    def test_roundtrip(self):
        with tempfile.TemporaryDirectory() as root:
            root=Path(root)
            self.assertTrue(generate(root))
            self.assertEqual(generate(root, check=True), [])

    def test_inventory_slot_count(self):
        self.assertEqual(SLOTS,36)
        init=resources()['datapack/data/npcraft/function/agent/init.mcfunction']
        self.assertEqual(init.count('data.agent.bag append value {}'),36)

    def test_transaction_order(self):
        r=resources()
        p='datapack/data/npcraft/function/'
        mine=r[p+'action/commit.mcfunction']
        self.assertLess(mine.index('run setblock'),mine.index('inventory/commit'))
        give=r[p+'inventory/give_held.mcfunction']
        self.assertLess(give.index('item replace'),give.index('function npcraft:inventory/commit'))
        for name in RECIPES:
            text=r[p+'craft/recipes/'+name+'.mcfunction']
            self.assertLess(text.index('inventory/take_staged'),text.index('inventory/add_staged'))
            self.assertLess(text.index('inventory/add_staged'),text.index('inventory/commit'))

    def test_recipe_graph_known_leaves(self):
        for name, (output,maximum,station,inputs) in RECIPES.items():
            self.assertGreater(output,0)
            self.assertGreaterEqual(maximum,output)
            for item,amount in inputs:
                self.assertIn(item,set(RECIPES)|{'oak_log','cobblestone'})
                self.assertGreater(amount,0)

    def test_mutation_boundaries(self):
        r=resources()
        mutators={p for p,t in r.items() if 'run setblock' in t}
        self.assertEqual(mutators,{'datapack/data/npcraft/function/action/commit.mcfunction','datapack/data/npcraft/function/action/place_table.mcfunction'})
        self.assertTrue(all('forceload' not in text for text in r.values()))

    def test_scalar_macro_and_paths(self):
        for path,text in resources().items():
            self.assertTrue(path.startswith('datapack/data/npcraft/'))
            self.assertNotIn('..',Path(path).parts)
            if path.endswith('.mcfunction'):
                for line in text.splitlines():
                    if '$(' in line:
                        self.assertTrue(line.lstrip().startswith('$'),(path,line))


class WorkflowContractTests(unittest.TestCase):
    def test_required_includes_graphical_and_runtime(self):
        from tools.generate_agent import ROOT
        workflow=(ROOT/'.github/workflows/ci.yml').read_text()
        self.assertIn('needs: [quality, vanilla, client]', workflow)
        self.assertIn('python tools/generate_agent.py --check', workflow)
        self.assertIn('python tools/agent_test.py --accept-eula', workflow)
        self.assertIn('test "$CLIENT" = success', workflow)
        self.assertIn('uses: ./.github/workflows/client-playtest.yml',workflow)

    def test_graphical_workflow_readonly_and_complete(self):
        from tools.generate_agent import ROOT
        workflow=(ROOT/'.github/workflows/client-playtest.yml').read_text()
        self.assertIn('workflow_call:',workflow)
        self.assertIn('python tools/client_playtest.py --accept-eula',workflow)
        self.assertIn('python tools/agent_playtest.py --accept-eula',workflow)
        self.assertNotIn('contents: write',workflow)
        self.assertNotIn('pull_request_target',workflow)
        self.assertNotIn('git push',workflow)
