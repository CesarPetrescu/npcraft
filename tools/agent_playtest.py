#!/usr/bin/env python3
"""Real-client autonomous progression and vertical-traversal acceptance.

The scene is an explicit creative-mode fixture. Only player input starts the agent;
RCON never calls its planner/crafting/mining routines to drive gameplay progress.
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
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.client_playtest import Client, PLAYER, BOT
from tools.client_install import install
from tools.build import ROOT, build
from tools.server_test import Server, download_server


def run(args):
    reports=args.reports.resolve();reports.mkdir(parents=True,exist_ok=True)
    result={'minecraft':'26.3','source_commit':os.environ.get('GITHUB_SHA','local'),
            'run_id':os.environ.get('GITHUB_RUN_ID'),'checks':[],'success':False,
            'method':'unmodified vanilla client input; independent loopback RCON assertions'}
    meta,cp,natives=install('26.3',args.cache.resolve()/'client')
    jar=download_server('26.3',args.cache.resolve()/'server')
    with tempfile.TemporaryDirectory(prefix='npcraft-agent-gui-') as temporary:
        root=Path(temporary)
        server=Server(root/'server',jar,build(),reports)
        props=server.work/'server.properties'
        settings=dict(line.split('=',1) for line in props.read_text().splitlines())
        settings.update({'gamemode':'creative','difficulty':'peaceful','enforce-secure-profile':'false'})
        props.write_text(''.join(f'{k}={v}\n' for k,v in settings.items()))
        client=Client(args.cache.resolve()/'client',root/'client',reports,int(settings['server-port']))
        def check(name,condition,truth=True):
            server.expect(condition,truth)
            result['checks'].append({'name':name,'passed':True})
            print('PASS '+name,flush=True)
        def wait(condition,timeout=180):
            end=time.monotonic()+timeout
            while time.monotonic()<end:
                try:server.expect(condition);return
                except AssertionError:time.sleep(0.3)
            server.expect(condition)
        def frame(name):
            server.command('tick freeze')
            try:
                server.command(f'execute at {BOT} run tp {PLAYER} ~3 ~ ~3 135 8')
                client.key('F1');client.shot(name);client.key('F1')
            finally:server.command('tick unfreeze')
        try:
            server.start();c=server.command
            c('forceload add -32 -32 32 32');time.sleep(3)
            c('fill -12 63 -12 20 63 12 minecraft:grass_block')
            c('fill -12 64 -12 20 72 12 minecraft:air')
            c('setworldspawn 0 64 5');c('time set noon');c('weather clear')
            for x,z in [(2,1),(2,-1)]:
                c(f'fill {x} 64 {z} {x} 67 {z} minecraft:oak_log')
                c(f'fill {x-1} 68 {z-1} {x+1} 68 {z+1} minecraft:oak_leaves[persistent=true]')
            for x,z in [(3,z) for z in range(-3,4)]+[(-3,z) for z in range(-3,4)]+[(-2,-3),(-1,-3)]:
                c(f'setblock {x} 64 {z} minecraft:stone')
            c('fill -4 63 -4 4 63 -4 minecraft:birch_planks')
            c('fill -4 63 4 4 63 4 minecraft:birch_planks')
            c('fill -4 63 -3 -4 63 3 minecraft:birch_planks')
            c('fill 4 63 -3 4 63 3 minecraft:birch_planks')
            c('setblock -6 64 0 minecraft:oak_log')
            c('fill 8 64 -1 11 64 1 minecraft:stone_bricks')
            c('fill 9 65 -1 11 65 1 minecraft:stone_bricks')
            client.start(meta,cp,natives)
            end=time.monotonic()+150
            while time.monotonic()<end:
                if client.process.poll() is not None:raise RuntimeError('Graphical client exited')
                client.focus()
                if PLAYER in c('list'):break
                time.sleep(2)
            else:raise TimeoutError('Client did not connect')
            time.sleep(8);client.focus()
            check('actual_client_connected',f'if entity @a[name={PLAYER}]')
            c(f'execute as {PLAYER} run function npcraft:admin/grant')
            c(f'tp {PLAYER} -0.5 64 3.5 180 0')
            client.chat('/trigger npcraft set 2')
            check('recruited_via_non_operator_client',f'if entity {BOT}')
            check('no_starting_tool',f'if data entity {BOT} data.tool',False)
            c(f'tp {PLAYER} 0.5 64 0.5 180 0');client.chat('/trigger npcraft set 8')
            c(f'tp {PLAYER} 5.5 64 6.5 135 5')
            client.chat('/trigger npcraft set 20')
            check('new_bag_starts_empty',f'if data entity {BOT} data.agent.bag[].item',False)
            client.shot('01-agent-management-panel');client.key('Escape')
            # The only instruction: work toward the kit. No resource/tool gifts follow.
            client.chat('/trigger npcraft set 21')
            check('autonomy_enabled_from_client',f'if score {BOT} np.mode matches 4')
            wait(f'if data entity {BOT} data.agent.bag[{{item:{{id:"minecraft:wooden_pickaxe"}}}}]',120)
            check('wooden_pickaxe_crafted_without_gift',f'if data entity {BOT} data.agent.bag[{{item:{{id:"minecraft:wooden_pickaxe"}}}}]')
            wait(f'if score {BOT} np.status matches 3',30)
            frame('02-autonomous-stone-mining')
            wait(f'if data entity {BOT} data.agent{{task:"stone_kit_ready"}}',240)
            for item in ('stone_pickaxe','stone_sword','stone_axe','furnace'):
                check('crafted_'+item,f'if data entity {BOT} data.agent.bag[{{item:{{id:"minecraft:{item}",count:1}}}}]')
            check('real_workbench_placed','if block 0 64 0 minecraft:crafting_table')
            check('nineteen_world_blocks_accounted',f'if data entity {BOT} data.agent{{mined:19}}')
            check('outside_plot_log_preserved','if block -6 64 0 minecraft:oak_log')
            result['completed_backpack']=c(f'data get entity {BOT} data.agent.bag')
            frame('03-stone-kit-complete')
            # Simulate one lost tool, not a new goal command. Replanning must replace it.
            c(f'data modify entity {BOT} data.agent.bag[{{item:{{id:"minecraft:stone_sword"}}}}] set value {{}}')
            c('setblock -3 64 -3 minecraft:stone');c('setblock -2 64 -3 minecraft:stone')
            wait(f'if data entity {BOT} data.agent.bag[{{item:{{id:"minecraft:stone_sword"}}}}]',120)
            check('lost_sword_replaced_without_new_order',f'if data entity {BOT} data.agent{{mined:21}}')
            # Stop, return actual produced items, inspect them in the ordinary survival inventory.
            client.chat('/trigger npcraft set 25')
            check('stop_from_client',f'if score {BOT} np.mode matches 0')
            c(f'execute at {BOT} run tp {PLAYER} ~ ~ ~')
            client.chat('/trigger npcraft set 23');time.sleep(2)
            check('backpack_drained_without_duplicate',f'if data entity {BOT} data.agent.bag[].item',False)
            for item in ('stone_pickaxe','stone_sword','stone_axe','furnace'):
                check('returned_'+item,f'if data entity {PLAYER} Inventory[{{id:"minecraft:{item}"}}]')
            c(f'gamemode survival {PLAYER}')
            client.key('e');client.shot('04-produced-items-in-player-inventory');client.key('Escape')
            # Store a component-bearing stack through the new public inventory command.
            c(f'item replace entity {PLAYER} weapon.mainhand with minecraft:iron_axe[minecraft:damage=11,minecraft:custom_name={{text:"Backpack QA"}}]')
            client.chat('/trigger npcraft set 22')
            check('new_backpack_transfer_removes_source',f'if items entity {PLAYER} weapon.mainhand minecraft:iron_axe',False)
            check('backpack_components_preserved',f'if data entity {BOT} data.agent.bag[{{item:{{id:"minecraft:iron_axe",components:{{"minecraft:damage":11}}}}}}]')
            # Real scheduled follow, not calls to the pathfinder from RCON.
            c(f'gamemode creative {PLAYER}');c(f'tp {PLAYER} 10.5 66 0.5 90 5')
            client.chat('/trigger npcraft set 4')
            end=time.monotonic()+30
            while time.monotonic()<end:
                c(f'execute store result score #gui_y np.tmp run data get entity {BOT} Pos[1]')
                try:server.expect('if score #gui_y np.tmp matches 66');break
                except AssertionError:time.sleep(0.3)
            check('follow_climbed_two_one_block_steps','if score #gui_y np.tmp matches 66')
            client.chat('/trigger npcraft set 5')
            frame('05-companion-on-raised-terrace')
            c(f'tp {PLAYER} 6.5 64 2.5 90 5');client.chat('/trigger npcraft set 4')
            end=time.monotonic()+30
            while time.monotonic()<end:
                c(f'execute store result score #gui_y np.tmp run data get entity {BOT} Pos[1]')
                try:server.expect('if score #gui_y np.tmp matches 64');break
                except AssertionError:time.sleep(0.3)
            check('follow_descended_safely','if score #gui_y np.tmp matches 64')
            client.chat('/trigger npcraft set 5')
            c('reload');time.sleep(2)
            check('backpack_survives_reload',f'if data entity {BOT} data.agent.bag[{{item:{{id:"minecraft:iron_axe"}}}}]')
            server.assert_clean_logs();result['success']=True
        except Exception as exc:
            result['failure']=str(exc);result['traceback']=traceback.format_exc()
            print(traceback.format_exc(),flush=True)
            with suppress(Exception):client.shot('failure')
            with suppress(Exception):result['state']=server.command(f'data get entity {BOT} data')
        finally:
            with suppress(Exception):server.command('tick unfreeze')
            client.stop();server.stop()
            result['screenshots']=sorted(x.name for x in (reports/'screenshots').glob('*.png')) if (reports/'screenshots').exists() else []
            (reports/'agent-results.json').write_text(json.dumps(result,indent=2)+'\n')
    return int(not result['success'])

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--accept-eula',action='store_true')
    parser.add_argument('--cache',type=Path,default=ROOT/'.cache/visual')
    parser.add_argument('--reports',type=Path,default=ROOT/'reports/agent-visual')
    args=parser.parse_args()
    if not args.accept_eula:parser.error('Explicit EULA acceptance is required')
    raise SystemExit(run(args))
