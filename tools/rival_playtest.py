#!/usr/bin/env python3
"""Graphical acceptance for empty-to-iron progression and opt-in mortal rivals.

The official client sends player requests. Console commands construct a disclosed
fixture, position cameras, and independently check behavior. No completed tools,
stations, fuel or ingots are injected into the autonomous progression inventory.
"""
from __future__ import annotations
import argparse
from contextlib import suppress
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import traceback
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.client_playtest import Client
from tools.client_install import install
from tools.server_test import ROOT, Server, download_server
from tools.build import build

PLAYER='NPCraftQA'
BOT='@e[type=minecraft:marker,tag=npcraft.bot,scores={np.id=1},limit=1]'
BODY='@e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=1},limit=1]'


def run(args):
    reports=args.reports.resolve();reports.mkdir(parents=True,exist_ok=True)
    result={'minecraft':'26.3','source_commit':os.environ.get('GITHUB_SHA','local'),
            'run_id':os.environ.get('GITHUB_RUN_ID'),'checks':[],'screenshots':[],'success':False,
            'method':'official GUI/xdotool; declared creative resource fixture, then survival duel; independent RCON checks'}
    meta,cp,natives=install('26.3',args.cache.resolve()/'client')
    jar=download_server('26.3',args.cache.resolve()/'server')
    with tempfile.TemporaryDirectory(prefix='npcraft-v03-gui-') as tmp:
        root=Path(tmp);server=Server(root/'server',jar,build(),reports)
        props=server.work/'server.properties';settings=dict(x.split('=',1) for x in props.read_text().splitlines())
        settings.update({'enforce-secure-profile':'false','gamemode':'creative','difficulty':'peaceful','max-players':'2','view-distance':'4'})
        props.write_text(''.join(f'{k}={v}\n' for k,v in settings.items()))
        client=Client(args.cache.resolve()/'client',root/'client',reports,int(settings['server-port']))
        other=None
        def check(name,condition,truth=True):
            server.expect(condition,truth);result['checks'].append({'name':name,'passed':True});print('PASS '+name,flush=True)
        def wait(name,condition,timeout=30):
            deadline=time.monotonic()+timeout
            while time.monotonic()<deadline:
                try:server.expect(condition);break
                except AssertionError:time.sleep(.3)
            else:raise AssertionError(name+' timed out: '+server.command(f'data get entity {BOT} data'))
            check(name,condition)
        def value(entity,path):
            response=server.command(f'data get entity {entity} {path}')
            match=re.search(r'data:\s*(-?\d+(?:\.\d+)?)',response)
            if not match:raise AssertionError(response)
            return float(match.group(1))
        def photograph(name):
            target=[value(BOT,f'Pos[{i}]') for i in range(3)]
            camera=(8.5,64.,7.5)
            dx,dy,dz=target[0]-camera[0],target[1]+1.2-(camera[1]+1.62),target[2]-camera[2]
            yaw=math.degrees(math.atan2(-dx,dz));pitch=-math.degrees(math.atan2(dy,math.hypot(dx,dz)))
            server.command(f'tp {PLAYER} {camera[0]} {camera[1]} {camera[2]} {yaw} {pitch}')
            client.key('F1');client.shot(name);client.key('F1')
        try:
            server.start();c=server.command
            c('forceload add -32 -32 32 32');time.sleep(3)
            c('fill -12 63 -12 22 63 12 minecraft:grass_block')
            c('fill -12 64 -12 22 71 12 minecraft:air')
            c('setworldspawn 0 64 6');c('time set noon');c('weather clear')
            c('gamerule minecraft:advance_time false');c('gamerule minecraft:advance_weather false')
            for x in (-3,3):
                c(f'fill {x} 64 -3 {x} 67 -3 minecraft:oak_log')
                c(f'fill {x-1} 68 -4 {x+1} 68 -2 minecraft:oak_leaves[persistent=true]')
            for x,z in [(-3,-1),(-3,1),(-3,3),(3,-1),(3,1),(3,3)]:c(f'fill {x} 64 {z} {x} 67 {z} minecraft:stone')
            for x,z in [(-2,-3),(0,-3),(2,-3),(-2,3),(2,3)]:c(f'setblock {x} 64 {z} minecraft:iron_ore')
            c('setblock 0 64 3 minecraft:coal_ore')
            c('setblock -5 64 0 minecraft:oak_log')
            client.start(meta,cp,natives)
            deadline=time.monotonic()+150
            while time.monotonic()<deadline:
                client.focus()
                if PLAYER in c('list'):break
                if client.process.poll() is not None:raise RuntimeError('Client exited')
                time.sleep(2)
            else:raise TimeoutError('Client did not join')
            time.sleep(8)
            c(f'execute as {PLAYER} run function npcraft:admin/grant')
            c(f'tp {PLAYER} 0.5 64 0.5 180 0')
            client.chat('/trigger npcraft set 2');client.chat('/trigger npcraft set 8')
            check('empty_backpack_start',f'if data entity {BOT} data.inventory.slots[].item',False)
            check('no_prebuilt_workbench_record',f'if data entity {BOT} data.agent.bench',False)
            c(f'tp {PLAYER} 7.5 64 7.5 135 5')
            client.chat('/trigger npcraft set 30');client.shot('01-iron-and-rival-controls');client.key('Escape')
            client.chat('/trigger npcraft set 31')
            check('iron_goal_requested_from_client',f'if score {BOT} np.mode matches 5')
            wait('self_sufficient_iron_pickaxe',f'if data entity {BOT} data.agent{{reason:"iron_pickaxe_obtained"}}',180)
            check('real_table_built',f'if data entity {BOT} data.agent.bench{{owned:1b}}')
            check('real_furnace_built',f'if data entity {BOT} data.agent.furnace{{owned:1b}}')
            check('iron_pick_stored',f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:iron_pickaxe",count:1}}')
            check('outside_log_untouched','if block -5 64 0 minecraft:oak_log')
            check('iron_pick_displayed',f'if items entity {BODY} weapon.mainhand minecraft:iron_pickaxe')
            result['iron_inventory']=c(f'data get entity {BOT} data.inventory')
            result['built_furnace']=c(f'data get entity {BOT} data.agent.furnace')
            photograph('02-self-built-workstations-and-iron-pick')
            client.chat('/trigger npcraft set 32');client.shot('03-authoritative-backpack-view');client.key('Escape')
            # Food is a disclosed separate survival-test supply, not a progression resource grant.
            c(f'item replace entity {PLAYER} weapon.mainhand with minecraft:bread 4')
            client.chat('/trigger npcraft set 21')
            check('food_transferred_from_client',f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:bread",count:4}}')
            c(f'gamemode survival {PLAYER}');c('difficulty normal')
            client.chat('/trigger npcraft set 40');client.shot('04-explicit-duel-consent');client.key('Escape')
            client.chat('/trigger npcraft set 41')
            check('duel_opted_in',f'if data entity {BOT} data.rival{{enabled:1b}}')
            check('body_is_mortal',f'if data entity {BODY} {{Invulnerable:0b}}')
            # Keep opponent out of sight while the rival finishes its own sword recipe.
            c(f'gamemode spectator {PLAYER}')
            wait('rival_crafts_own_iron_sword',f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:iron_sword"}}',100)
            c('function npcraft:admin/pause')
            c(f'gamemode survival {PLAYER}')
            c(f'tp {BOT} 0.5 64 7.5')
            c(f'execute as {BOT} at @s run function npcraft:bot/sync with entity @s data')
            c(f'tp {PLAYER} 0.5 64 9.5 180 0')
            c(f'execute as {BOT} run data remove entity @s data.navigation')
            c('function npcraft:admin/resume')
            before=value(PLAYER,'Health')
            deadline=time.monotonic()+5
            while time.monotonic()<deadline and value(PLAYER,'Health')>=before:time.sleep(.2)
            after=value(PLAYER,'Health')
            if not after<before:raise AssertionError('Consenting player was not hit')
            result['observed_pvp_damage']={'before':before,'after':after}
            check('weapon_wears_on_real_hit',f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:iron_sword",components:{{"minecraft:damage":1}}}}')
            # Stop from outside both the action range and arena; this must not require proximity.
            c(f'tp {PLAYER} 25.5 64 0.5')
            client.chat('/trigger npcraft set 42')
            check('remote_consent_revocation',f'if data entity {BOT} data.rival{{enabled:0b}}')
            c(f'gamemode creative {PLAYER}');c(f'execute as {PLAYER} run effect give @s minecraft:instant_health 1 5')
            c('function npcraft:admin/pause')
            # Re-enable while hidden behind an opaque wall, then exercise exact last-seen memory.
            c(f'tp {BOT} 0.5 64 7.5');c(f'execute as {BOT} at @s run function npcraft:bot/sync with entity @s data')
            c(f'tp {PLAYER} 0.5 64 10.5 180 0');c(f'gamemode survival {PLAYER}')
            c('function npcraft:admin/resume');client.chat('/trigger npcraft set 41')
            c('function npcraft:admin/pause')
            c(f'execute as {BOT} at @s run function npcraft:rival/perceive with entity @s data.rival')
            c(f'data modify storage npcraft:qa last_seen set from entity {BOT} data.rival.last')
            c('fill -3 64 9 3 67 9 minecraft:stone_bricks')
            c(f'tp {PLAYER} 2.5 64 11.5 180 0')
            c(f'execute as {BOT} at @s run function npcraft:rival/perceive with entity @s data.rival')
            check('wall_blocks_current_vision','if score #seen np.tmp matches 0')
            c(f'data modify storage npcraft:qa compared set from entity {BOT} data.rival.last')
            c('execute store success score #seen_changed np.tmp run data modify storage npcraft:qa compared set from storage npcraft:qa last_seen')
            check('hidden_position_not_leaked_to_memory','if score #seen_changed np.tmp matches 0')
            hp=value(PLAYER,'Health')
            for _ in range(3):c(f'execute as {BOT} at @s run function npcraft:rival/attack with entity @s data')
            if value(PLAYER,'Health')!=hp:raise AssertionError('Damage through wall')
            result['checks'].append({'name':'no_damage_through_wall','passed':True})
            # Withdraw immediately with the normal client, then mortality/meal tests.
            c('function npcraft:admin/resume');client.chat('/trigger npcraft set 42')
            c(f'gamemode creative {PLAYER}')
            c(f'execute as {BOT} run data modify entity @s data.survival.food set value 8')
            c(f'damage {BODY} 6 minecraft:generic')
            wait('supplied_food_consumed',f'if data entity {BOT} data.survival{{food:13}}',5)
            check('meal_heals_native_body',f'if data entity {BODY} {{Health:16.0f}}')
            photograph('05-mortal-rival-test-area')
            # Avoid the nearby creative player auto-collecting the corpse's legitimate drops.
            c(f'tp {PLAYER} 8.5 64 7.5 90 0')
            c(f'damage {BODY} 100 minecraft:generic')
            wait('death_recorded',f'if data entity {BOT} data.survival{{dead:1b,deaths:1}}',5)
            check('corpse_inventory_cleared',f'if data entity {BOT} data.inventory.slots[].item',False)
            check('earned_iron_pick_dropped','if entity @e[type=minecraft:item,nbt={Item:{id:"minecraft:iron_pickaxe"}}]')
            check('no_visual_copy_loot','if entity @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{npcraft_visual:1b}}}}]',False)
            photograph('06-real-inventory-drops-on-death')
            wait('safe_empty_respawn',f'if data entity {BOT} data.survival{{dead:0b}}',20)
            check('no_free_replacement_pick',f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:iron_pickaxe"}}',False)
            c('save-all flush');server.assert_clean_logs()
            result['success']=True
        except Exception as exc:
            result['failure']=str(exc);result['traceback']=traceback.format_exc();print(result['traceback'],flush=True)
            with suppress(Exception):client.shot('failure');result['state']=server.command(f'data get entity {BOT} data')
        finally:
            with suppress(Exception):server.command('tick unfreeze')
            if other:other.stop()
            client.stop();server.stop()
            result['screenshots']=sorted(p.name for p in (reports/'screenshots').glob('*.png')) if (reports/'screenshots').exists() else []
            (reports/'rival-results.json').write_text(json.dumps(result,indent=2)+'\n')
    return int(not result['success'])

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--accept-eula',action='store_true')
    p.add_argument('--cache',type=Path,default=ROOT/'.cache/visual');p.add_argument('--reports',type=Path,default=ROOT/'reports/rival-visual')
    args=p.parse_args()
    if not args.accept_eula:p.error('Explicit --accept-eula is required')
    raise SystemExit(run(args))
