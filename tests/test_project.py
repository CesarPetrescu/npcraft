"""Offline tests for packaging, negative lint cases and RCON packet handling."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
import struct
import tempfile
import unittest
from unittest.mock import Mock
import zipfile
from tools.build import ROOT, build
from tools.validate import validate, unique_object
from tools.server_test import Rcon, TESTS


class ProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / 'datapack', self.root / 'datapack')
        shutil.copy2(ROOT / 'project.json', self.root / 'project.json')

    def tearDown(self):
        self.temp.cleanup()

    def test_structure(self):
        self.assertEqual(validate(self.root), [])

    def test_archive_is_directly_installable(self):
        with zipfile.ZipFile(build(self.root)) as zf:
            self.assertIn('pack.mcmeta', zf.namelist())
            self.assertIn('data/minecraft/tags/function/load.json', zf.namelist())
            self.assertTrue(all(not name.startswith(('datapack/', '/', '../')) for name in zf.namelist()))
            self.assertIsNone(zf.testzip())

    def test_archive_reproducible(self):
        first = build(self.root, self.root / 'a').read_bytes()
        second = build(self.root, self.root / 'b').read_bytes()
        self.assertEqual(first, second)

    def test_archive_checksum(self):
        path = build(self.root)
        self.assertEqual(path.with_suffix('.zip.sha256').read_text().split()[0], hashlib.sha256(path.read_bytes()).hexdigest())

    def test_build_does_not_include_repository(self):
        (self.root / 'sensitive.env').write_text('not distributable')
        with zipfile.ZipFile(build(self.root)) as zf:
            self.assertNotIn('sensitive.env', zf.namelist())

    def mutate(self, relative, text):
        path = self.root / 'datapack' / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return validate(self.root)

    def test_reject_missing_function(self):
        issues = self.mutate('data/npcraft/function/bad.mcfunction', 'function npcraft:missing\n')
        self.assertTrue(any('Unresolved function' in item for item in issues))

    def test_reject_missing_macro_prefix(self):
        issues = self.mutate('data/npcraft/function/bad.mcfunction', 'tp @s $(x) 64 0\n')
        self.assertTrue(any('macro prefix' in item for item in issues))

    def test_reject_missing_tag(self):
        issues = self.mutate('data/npcraft/function/bad.mcfunction', 'execute if block ~ ~ ~ #npcraft:missing run return 1\n')
        self.assertTrue(any('block tag' in item for item in issues))

    def test_reject_navigation_block_mutation(self):
        issues = self.mutate('data/npcraft/function/nav/bad.mcfunction', 'setblock ~ ~-1 ~ minecraft:air\n')
        self.assertTrue(any('Navigation may not mutate' in item for item in issues))

    def test_reject_force_loading(self):
        issues = self.mutate('data/npcraft/function/bad.mcfunction', 'execute in minecraft:overworld run forceload add ~ ~\n')
        self.assertTrue(any('Forbidden' in item for item in issues))

    def test_reject_privileged_dialog(self):
        obj={'type':'minecraft:multi_action','actions':[{'label':'No','action':{'type':'run_command','command':'op @s'}}]}
        issues=self.mutate('data/npcraft/dialog/bad.json',json.dumps(obj)+'\n')
        self.assertTrue(any('privileged' in item for item in issues))

    def test_reject_duplicate_json(self):
        with self.assertRaises(ValueError):
            json.loads('{"a":1,"a":2}', object_pairs_hook=unique_object)

    def test_reject_invalid_json(self):
        issues=self.mutate('data/npcraft/dialog/bad.json','{bad}\n')
        self.assertTrue(issues)

    def test_reject_plural_directories(self):
        issues=self.mutate('data/npcraft/functions/bad.mcfunction','return 1\n')
        self.assertTrue(any('Legacy plural' in item for item in issues))

    def test_reject_metadata_drift(self):
        path=self.root/'project.json'
        data=json.loads(path.read_text());data['pack_format']=[88,0];path.write_text(json.dumps(data))
        self.assertTrue(any('format must match' in item for item in validate(self.root)))

    def test_reject_symlink(self):
        (self.root/'datapack/link.json').symlink_to(self.root/'project.json')
        self.assertTrue(any('Symlink' in item for item in validate(self.root)))
        with self.assertRaises(ValueError):build(self.root)

    def test_reject_unexpected_pack_file(self):
        self.mutate('secret.env','secret\n')
        with self.assertRaises(ValueError):build(self.root)

    def test_reject_unsafe_version(self):
        path=self.root/'project.json';data=json.loads(path.read_text());data['version']='../../escape';path.write_text(json.dumps(data))
        with self.assertRaises(ValueError):build(self.root)

    def test_safety_contracts_present(self):
        base=self.root/'datapack/data/npcraft/function'
        auth=(base/'commands/authorize.mcfunction').read_text()
        self.assertIn('np.owner = #actor',auth)
        self.assertIn('UUID:$(owner_uuid)',auth)
        nav=(base/'nav/neighbor.mcfunction').read_text()
        self.assertIn('matches 128..',nav)
        self.assertIn('distance=..6',nav)
        self.assertIn('unless function npcraft:nav/cell_safe',nav)
        self.assertIn('unless loaded',(base/'nav/cell_safe.mcfunction').read_text())
        commit=(base/'work/commit.mcfunction').read_text()
        self.assertLess(commit.index('run setblock'),commit.index('data.cargo set value'))
        self.assertIn('unless function npcraft:work/in_bounds',commit)
        self.assertIn('matches 64..',commit)

    def test_navigation_coordinates_and_parent_selection(self):
        base=self.root/'datapack/data/npcraft/function'
        for relative in ('nav/goal.mcfunction', 'work/sight.mcfunction'):
            self.assertIn('$(z) align xyz positioned ~0.5', (base/relative).read_text())
        search=(base/'nav/search.mcfunction').read_text()
        self.assertIn('scoreboard players operation #min np.tmp < @e[tag=npcraft.open] np.depth', search)
        self.assertIn('tag @e[tag=npcraft.frontier,limit=1] add npcraft.current_node', search)
        self.assertNotIn('unless entity @e[tag=npcraft.current_node]', search)

    def test_vanilla_suite_has_behavioral_coverage(self):
        names={test.__name__ for test in TESTS}
        self.assertGreaterEqual(len(names),20)
        self.assertTrue({'test_persistence','test_full_barrel_and_transfer','test_wall_detour','test_unauthorized_and_offline'}.issubset(names))


class RconTests(unittest.TestCase):
    def test_split_reads(self):
        client=Rcon.__new__(Rcon);client.socket=Mock()
        client.socket.recv.side_effect=[b'a',b'bc']
        self.assertEqual(client._read_exactly(3),b'abc')

    def test_eof(self):
        client=Rcon.__new__(Rcon);client.socket=Mock();client.socket.recv.return_value=b''
        with self.assertRaises(ConnectionError):client._read_exactly(1)

    def test_packet_round_trip(self):
        client=Rcon.__new__(Rcon);client.socket=Mock();client.sequence=0
        body=struct.pack('<ii',1,0)+b'hello\0\0'
        client.socket.recv.side_effect=[struct.pack('<i',len(body)),body]
        self.assertEqual(client.request('list'),'hello')
        sent=client.socket.sendall.call_args.args[0]
        self.assertEqual(struct.unpack('<iii',sent[:12]),(14,1,2))

    def test_packet_length_guard(self):
        client=Rcon.__new__(Rcon);client.socket=Mock();client.sequence=0
        client.socket.recv.return_value=struct.pack('<i',-1)
        with self.assertRaises(ConnectionError):client.request('list')


if __name__=='__main__':unittest.main()
