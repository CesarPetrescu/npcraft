#!/usr/bin/env python3
"""Run real autonomous rival-kit progression at 1/4/8/16 allocations.

All resources are declared fixtures in isolated force-loaded test chunks. Controllers
use production runtime/planning, no online owner and no per-action driver. Tick sprint
accelerates the run; it is NOT a player-latency, GPU or natural-world benchmark.
"""
from __future__ import annotations
import argparse
from contextlib import suppress
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import sys
import tempfile
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.server_test import ROOT, Server, download_server
from tools.build import build


def score(server, name):
    answer = server.command(f'scoreboard players get {name} np.tmp')
    m = re.search(r'has (-?\d+) \[np\.tmp\]', answer)
    if m is None: raise AssertionError(answer)
    return int(m.group(1))


def prepare(s, count):
    c=s.command
    c('function npcraft:admin/pause')
    c('forceload add -16 -16 64 64')
    deadline=time.monotonic()+25
    while time.monotonic()<deadline:
        try:
            s.expect('if loaded -8 64 -8 if loaded 54 64 54');break
        except AssertionError:time.sleep(.2)
    else:raise TimeoutError('Soak fixture chunks did not load')
    c('fill -8 63 -8 54 63 54 minecraft:grass_block')
    c('fill -8 64 -8 54 70 54 minecraft:air')
    c('difficulty peaceful');c('time set noon')
    c('data modify storage npcraft:state queue set value []')
    c('function npcraft:rival/acl_write {id:1,allowed:1b}')
    c('function npcraft:rival/consent_write {id:1,token:1}')
    width=math.ceil(math.sqrt(count))
    for i in range(count):
        x,z=(i%width)*14,(i//width)*14
        ident=9100+i
        bot=f'@e[type=minecraft:marker,tag=npcraft.soak,scores={{np.id={ident}}},limit=1]'
        for dx in (-3,3):c(f'fill {x+dx} 64 {z-3} {x+dx} 67 {z-3} minecraft:oak_log')
        for dx,dz in [(-3,-1),(-3,1),(-3,3),(3,-1),(3,1),(3,3)]:
            c(f'fill {x+dx} 64 {z+dz} {x+dx} 67 {z+dz} minecraft:stone')
        for dx,dz in [(-2,-3),(0,-3),(2,-3),(-2,3),(2,3)]:c(f'setblock {x+dx} 64 {z+dz} minecraft:iron_ore')
        c(f'setblock {x} 64 {z+3} minecraft:coal_ore')
        c(f'summon minecraft:marker {x+.5} 64 {z+.5} {{Tags:["npcraft.bot","npcraft.soak","npcraft.new"],data:{{schema:1,id:{ident},owner:1,owner_uuid:[I;0,0,0,1],home:{{x:{x},y:64,z:{z}}},plot:{{x:{x},y:64,z:{z}}},scan:0,scanned:0,rival:{{enabled:1b,token:1,retreat:0b,react_at:0,attack_at:0,seen_at:-1000,center:{{x:{x},y:64,z:{z}}},opponent:[I;0,0,0,1]}}}}}}')
        c(f'scoreboard players set @e[tag=npcraft.new,limit=1] np.id {ident}')
        c('tag @e[tag=npcraft.new] remove npcraft.new')
        for obj,val in [('np.owner',1),('np.mode',6),('np.next',0),('np.dig',0),('np.harvest',0),('np.status',0)]:c(f'scoreboard players set {bot} {obj} {val}')
        c(f'execute as {bot} at @s run function npcraft:agent/init')
        c(f'execute as {bot} at @s run function npcraft:bot/sync with entity @s data')
        c(f'data modify storage npcraft:state queue append value {{id:{ident}}}')
    # No online player is required to tick an opted-in loaded rival.
    s.expect('if entity @a',False)
    c('function npcraft:admin/resume')


def run_case(args, jar, archive, count):
    directory=args.reports/f'agents-{count}'
    directory.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='npcraft-soak-') as tmp:
        server=Server(Path(tmp),jar,archive,directory)
        result={'agents':count,'success':False,'resource_fixture':'separate 7x7 plots, logs/stone/5 iron/1 coal each','updates':'production tick + scheduler; tick sprint'}
        try:
            server.start();prepare(server,count)
            c=server.command
            c('execute store result score #begin np.tmp run time query gametime')
            c(f'tick sprint {args.ticks}t')
            start=time.monotonic();deadline=start+300
            last_progress=None
            while time.monotonic()<deadline:
                c('execute store result score #elapsed np.tmp run time query gametime')
                c('scoreboard players operation #elapsed np.tmp -= #begin np.tmp')
                elapsed=score(server,'#elapsed')
                c('execute store result score #complete np.tmp run execute if entity @e[tag=npcraft.soak,nbt={data:{agent:{reason:"rival_kit_obtained"}}}]')
                complete=score(server,'#complete')
                progress=(elapsed//500,complete)
                if progress!=last_progress:
                    print(f'Soak {count}: tick={elapsed}, completed={complete}/{count}',flush=True)
                    last_progress=progress
                if elapsed>=args.ticks:break
                time.sleep(.5)
            else:raise TimeoutError(f'{count} agents exceeded wall-clock timeout')
            with suppress(Exception):result['sprint_response']=c('tick sprint stop')
            result['tick_query']=c('tick query')
            result['wall_seconds']=round(time.monotonic()-start,3)
            c('function npcraft:admin/pause')
            result['completed']=complete
            if complete!=count:
                result['states']=[c(f'data get entity @e[tag=npcraft.soak,scores={{np.id={9100+i}}},limit=1] data') for i in range(count)]
                raise AssertionError(f'Only {complete}/{count} agents completed their rival kit')
            result['harvests']=[]
            for i in range(count):
                bot=f'@e[tag=npcraft.soak,scores={{np.id={9100+i}}},limit=1]'
                for kind in ('minecraft:iron_pickaxe','minecraft:iron_sword'):
                    server.expect(f'if data entity {bot} data.inventory.slots[].item{{id:"{kind}",count:1}}')
                c(f'scoreboard players operation #harvest np.tmp = {bot} np.harvest')
                result['harvests'].append(score(server,'#harvest'))
            # Strict conservation in this declared finite scenario, not a generated survival map.
            if result['harvests'] != [20]*count:raise AssertionError(f'Unexpected harvest accounting: {result["harvests"]}')
            server.expect('if entity @e[tag=npcraft.nav]',False)
            c('save-all flush');server.assert_clean_logs()
            result['success']=True
        except Exception as exc:
            result['failure']=str(exc)
            print(f'FAIL soak {count}: {exc}',flush=True)
        finally:
            with suppress(Exception):server.command('tick sprint stop')
            server.stop()
            (directory/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--accept-eula',action='store_true')
    p.add_argument('--agents',default='1,4,8,16')
    p.add_argument('--ticks',type=int,default=6000)
    p.add_argument('--reports',type=Path,default=ROOT/'reports/soak')
    p.add_argument('--cache',type=Path,default=ROOT/'.cache/vanilla')
    args=p.parse_args()
    if not args.accept_eula:p.error('Explicit EULA acceptance is required')
    counts=[int(n) for n in args.agents.split(',')]
    if not counts or any(n<1 or n>16 for n in counts):p.error('Agent counts must be between 1 and 16')
    if not 100<=args.ticks<=12000:p.error('Ticks must be bounded to 100..12000')
    args.reports=args.reports.resolve();args.reports.mkdir(parents=True,exist_ok=True)
    target=json.loads((ROOT/'project.json').read_text())
    jar=download_server(target['minecraft'],args.cache.resolve());archive=build()
    result={'source_commit':os.environ.get('GITHUB_SHA','local'),'run_id':os.environ.get('GITHUB_RUN_ID'),
            'platform':platform.platform(),'logical_cpus':os.cpu_count(),'ticks_per_case':args.ticks,
            'datapack_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
            'method':'accelerated production-runtime progression in isolated declared fixtures; no natural-world or latency claims',
            'cases':[run_case(args,jar,archive,n) for n in counts]}
    result['success']=all(c['success'] for c in result['cases'])
    (args.reports/'soak-results.json').write_text(json.dumps(result,indent=2)+'\n')
    return int(not result['success'])

if __name__=='__main__':raise SystemExit(main())
