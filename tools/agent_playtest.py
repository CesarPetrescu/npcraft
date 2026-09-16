#!/usr/bin/env python3
"""Exercise agent goals/inventory/vertical follow in the unmodified graphical client.

RCON constructs a disclosed creative test fixture and verifies results. Player
requests originate from actual GUI keyboard input, not console impersonation.
"""
from __future__ import annotations
import argparse
from contextlib import suppress
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import traceback

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.client_playtest import Client
from tools.client_install import install
from tools.server_test import ROOT, Server, download_server
from tools.build import build

PLAYER = 'NPCraftQA'
BOT = '@e[type=minecraft:marker,tag=npcraft.bot,scores={np.id=1},limit=1]'


def run(args):
    reports = args.reports.resolve()
    reports.mkdir(parents=True, exist_ok=True)
    result = {'minecraft': '26.3', 'source_commit': os.environ.get('GITHUB_SHA', 'local'),
              'run_id': os.environ.get('GITHUB_RUN_ID'), 'success': False, 'checks': [],
              'method': 'unmodified vanilla GUI, xdotool player requests, RCON fixture/assertions',
              'screenshots': []}
    def check(name, condition, truth=True):
        server.expect(condition, truth)
        result['checks'].append({'name': name, 'passed': True})
        print('PASS ' + name, flush=True)
    meta, cp, natives = install('26.3', args.cache.resolve() / 'client')
    jar = download_server('26.3', args.cache.resolve() / 'server')
    with tempfile.TemporaryDirectory(prefix='npcraft-agent-gui-') as tmp:
        root = Path(tmp)
        server = Server(root / 'server', jar, build(), reports)
        props = server.work / 'server.properties'
        settings = dict(line.split('=', 1) for line in props.read_text().splitlines())
        settings.update({'enforce-secure-profile': 'false', 'gamemode': 'creative',
                         'difficulty': 'peaceful', 'view-distance': '4'})
        props.write_text(''.join(f'{k}={v}\n' for k, v in settings.items()))
        client = Client(args.cache.resolve() / 'client', root / 'client', reports, int(settings['server-port']))
        try:
            server.start()
            c = server.command
            c('forceload add -32 -32 32 32')
            time.sleep(3)
            c('fill -12 63 -12 20 63 12 minecraft:grass_block')
            c('fill -12 64 -12 20 70 12 minecraft:air')
            c('setworldspawn 0 64 5')
            c('time set noon')
            c('weather clear')
            c('gamerule minecraft:advance_time false')
            c('gamerule minecraft:advance_weather false')
            # Two small trunks: only two logs are required by the planned recipes.
            for x in [-1, 1]:
                c(f'fill {x} 64 0 {x} 67 0 minecraft:oak_log')
                c(f'fill {x-1} 68 -1 {x+1} 68 1 minecraft:oak_leaves[persistent=true]')
            for x, z in [(-2, -1), (2, -1), (0, -2)]:
                c(f'setblock {x} 64 {z} minecraft:stone')
            c('setblock 0 63 3 minecraft:crafting_table')
            for line in ['fill -4 63 -4 4 63 -4 minecraft:birch_planks',
                         'fill -4 63 4 4 63 4 minecraft:birch_planks',
                         'fill -4 63 -3 -4 63 3 minecraft:birch_planks',
                         'fill 4 63 -3 4 63 3 minecraft:birch_planks']:
                c(line)
            c('setblock -5 64 0 minecraft:oak_log')  # Outside the permitted plot.
            # Full-block staircase, not slabs: three explicit one-block ascents.
            c('fill 8 64 -2 8 64 2 minecraft:stone_bricks')
            c('fill 9 64 -2 9 65 2 minecraft:stone_bricks')
            c('fill 10 64 -3 17 66 5 minecraft:stone_bricks')
            client.start(meta, cp, natives)
            deadline = time.monotonic() + 150
            while time.monotonic() < deadline:
                if client.process.poll() is not None:
                    raise RuntimeError('Minecraft client exited')
                client.focus()
                if PLAYER in c('list'):
                    break
                time.sleep(2)
            else:
                raise TimeoutError('Client did not join')
            time.sleep(8)
            c(f'execute as {PLAYER} run function npcraft:admin/grant')
            c(f'tp {PLAYER} 0.5 64 5.5 180 5')
            client.chat('/trigger npcraft set 2')
            check('client_recruited_agent', 'if entity ' + BOT)
            client.chat('/trigger npcraft set 20')
            client.shot('01-agent-controls')
            client.key('Escape')
            c(f'item replace entity {PLAYER} weapon.mainhand with minecraft:diamond[minecraft:custom_name={{text:"Backpack QA"}}] 20')
            c(f'data modify storage npcraft:gui original_stack set from entity {PLAYER} SelectedItem')
            client.chat('/trigger npcraft set 21')
            check('give_stack_removes_player_source', f'if items entity {PLAYER} weapon.mainhand minecraft:diamond', False)
            check('backpack_preserves_stack_count', f'if data entity {BOT} data.inventory.slots[0].item{{id:"minecraft:diamond",count:20}}')
            c(f'data modify storage npcraft:gui copied_stack set from entity {BOT} data.inventory.slots[0].item')
            c('execute store success score #gui_changed np.tmp run data modify storage npcraft:gui copied_stack set from storage npcraft:gui original_stack')
            check('backpack_preserves_exact_components', 'if score #gui_changed np.tmp matches 0')
            c(f'tp {PLAYER} 3.5 64 5.5 90 0')
            client.chat('/trigger npcraft set 22')
            check('backpack_return_preserves_count', 'if entity @e[type=minecraft:item,nbt={Item:{id:"minecraft:diamond",count:20}}]')
            check('backpack_return_clears_source', f'if data entity {BOT} data.inventory.slots[].item', False)
            c('kill @e[type=minecraft:item]')  # Remove only the already-verified fixture drops.
            c(f'tp {PLAYER} 0.5 64 0.5 180 0')
            client.chat('/trigger npcraft set 8')
            c(f'tp {PLAYER} 0.5 64 3.5 180 0')
            client.chat('/trigger npcraft set 24')
            check('real_workbench_assigned', f'if data entity {BOT} data.agent.bench{{x:0,y:63,z:3}}')
            c(f'tp {PLAYER} 4.5 64 7.5 140 5')
            client.key('F1')
            client.shot('02-empty-handed-goal-fixture')
            client.key('F1')
            client.chat('/trigger npcraft set 23')
            check('goal_request_accepted', f'if score {BOT} np.mode matches 4')
            seen = set()
            deadline = time.monotonic() + 120
            while time.monotonic() < deadline:
                intent = c(f'data get entity {BOT} data.agent.intent')
                seen.add(intent)
                if 'stone_pickaxe_obtained' in c(f'data get entity {BOT} data.agent.reason'):
                    break
                time.sleep(0.5)
            else:
                raise AssertionError('Autonomous stone-pickaxe goal timed out: ' + c(f'data get entity {BOT} data'))
            result['observed_intents'] = sorted(seen)
            check('stone_pickaxe_obtained_autonomously', f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:stone_pickaxe",count:1}}')
            check('wood_pick_wear_exactly_three', f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:wooden_pickaxe",components:{{"minecraft:damage":3}}}}')
            check('recipe_leftovers_exact', f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:oak_planks",count:3}}')
            check('five_blocks_harvested_total', f'if score {BOT} np.harvest matches 5')
            check('cobblestone_consumed_by_recipe', f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:cobblestone"}}', False)
            check('out_of_bounds_log_preserved', 'if block -5 64 0 minecraft:oak_log')
            result['completed_inventory'] = c(f'data get entity {BOT} data.inventory')
            c(f'execute at {BOT} run tp {PLAYER} ~3 ~ ~4 143 5')
            client.key('F1')
            client.shot('03-crafted-stone-pickaxe')
            client.key('F1')
            time.sleep(2)
            check('goal_stops_consuming_after_success', f'if score {BOT} np.harvest matches 5')
            client.chat('/trigger npcraft set 11')
            check('owner_can_cancel_agent', f'if data entity {BOT} data.agent{{state:"cancelled"}}')
            c(f'tp {PLAYER} 6.5 64 0.5 -90 0')
            client.chat('/trigger npcraft set 4')
            c(f'tp {PLAYER} 12.5 67 0.5 90 5')
            deadline = time.monotonic() + 25
            while time.monotonic() < deadline:
                try:
                    server.expect('if entity @e[tag=npcraft.bot,x=12.5,y=67,z=0.5,distance=..2.1]')
                    break
                except AssertionError:
                    time.sleep(0.5)
            else:
                raise AssertionError('Vertical follow failed: ' + c(f'data get entity {BOT} Pos'))
            check('follow_climbs_three_full_block_steps', 'if entity @e[tag=npcraft.bot,x=12.5,y=67,z=0.5,distance=..2.1]')
            check('navigation_preserved_stair_blocks', 'if block 8 64 0 minecraft:stone_bricks if block 9 65 0 minecraft:stone_bricks if block 10 66 0 minecraft:stone_bricks')
            client.chat('/trigger npcraft set 5')
            c(f'execute at {BOT} run tp {PLAYER} ~4 ~ ~4 135 5')
            client.key('F1')
            client.shot('04-vertical-follow-platform')
            client.key('F1')
            c('reload')
            time.sleep(2)
            check('inventory_survives_reload_with_client', f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:stone_pickaxe"}}')
            server.assert_clean_logs()
            result['success'] = True
        except Exception as exc:
            result['failure'] = str(exc)
            result['traceback'] = traceback.format_exc()
            print(result['traceback'], flush=True)
            with suppress(Exception):
                client.shot('failure')
                result['agent_state'] = server.command(f'data get entity {BOT} data')
        finally:
            client.stop()
            server.stop()
            result['screenshots'] = sorted(p.name for p in (reports / 'screenshots').glob('*.png')) if (reports / 'screenshots').exists() else []
            (reports / 'agent-results.json').write_text(json.dumps(result, indent=2) + '\n')
    return 0 if result['success'] else 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--accept-eula', action='store_true')
    parser.add_argument('--cache', type=Path, default=ROOT / '.cache/visual')
    parser.add_argument('--reports', type=Path, default=ROOT / 'reports/agent-visual')
    args = parser.parse_args()
    if not args.accept_eula:
        parser.error('Explicit --accept-eula is required')
    raise SystemExit(run(args))
