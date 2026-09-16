#!/usr/bin/env python3
"""Additional actual-vanilla acceptance fixtures for the autonomous agent module."""
from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools import server_test as base
BOT, AS = base.BOT, base.AS


def init(s):
    s.command(AS + 'function npcraft:agent/init')


def add(s, kind, count=1, maximum=64, components=''):
    init(s)
    extra = ',components:' + components if components else ''
    s.command(AS + f'data modify entity @s data.agent.request set value {{stack:{{id:"minecraft:{kind}",count:{count}{extra}}},max:{maximum}}}')
    s.command(AS + 'function npcraft:inventory/add')


def count(s, kind, amount):
    s.command(AS + f'function npcraft:inventory/count {{kind:"{kind}"}}')
    s.expect(f'if score #iv_have np.tmp matches {amount}')


def table(s):
    init(s)
    s.command('setblock 1 64 0 minecraft:crafting_table')
    s.command(AS + 'data modify entity @s data.agent.station set value {x:1,y:64,z:0}')


def test_bag_init(s):
    init(s)
    s.command(AS + 'execute store result score #length np.tmp run data get entity @s data.agent.bag')
    s.expect('if score #length np.tmp matches 36')
    add(s,'oak_log',7)
    init(s)
    count(s,'oak_log',7)


def test_merge_and_split(s):
    add(s,'oak_log',63)
    add(s,'oak_log',5)
    s.expect(f'if data entity {BOT} data.agent.bag[0].item{{count:64}}')
    s.expect(f'if data entity {BOT} data.agent.bag[1].item{{count:4}}')
    count(s,'oak_log',68)


def test_components_not_merged(s):
    add(s,'oak_log',2,components='{"minecraft:custom_name":{text:"A"}}')
    add(s,'oak_log',3,components='{"minecraft:custom_name":{text:"B"}}')
    s.expect(f'if data entity {BOT} data.agent.bag[0].item{{count:2}}')
    s.expect(f'if data entity {BOT} data.agent.bag[1].item{{count:3}}')
    s.expect(f'if data entity {BOT} data.agent.bag[0].item.components{{"minecraft:custom_name":{{text:"A"}}}}')


def test_stack_limit_16(s):
    add(s,'ender_pearl',19,16)
    s.expect(f'if data entity {BOT} data.agent.bag[0].item{{count:16}}')
    s.expect(f'if data entity {BOT} data.agent.bag[1].item{{count:3}}')


def test_full_bag_rollback(s):
    add(s,'oak_log',2304)
    s.expect('if score #iv_ok np.tmp matches 1')
    add(s,'cobblestone',1)
    s.expect('if score #iv_ok np.tmp matches 0')
    count(s,'oak_log',2304)
    count(s,'cobblestone',0)


def test_partial_merge_rollback(s):
    add(s,'oak_log',2303)
    add(s,'oak_log',2)
    s.expect('if score #iv_ok np.tmp matches 0')
    count(s,'oak_log',2303)


def test_invalid_add(s):
    add(s,'oak_log',0)
    s.expect('if score #iv_ok np.tmp matches 0')
    add(s,'oak_log',3,0)
    s.expect('if score #iv_ok np.tmp matches 0')
    count(s,'oak_log',0)


def test_recipe_consumes(s):
    add(s,'oak_log',2)
    s.command(AS + 'function npcraft:craft/recipes/oak_planks')
    count(s,'oak_log',1)
    count(s,'oak_planks',4)


def test_recipe_missing_rollback(s):
    table(s)
    add(s,'oak_planks',3)
    s.command(AS + 'function npcraft:craft/recipes/wooden_pickaxe')
    count(s,'oak_planks',3)
    count(s,'wooden_pickaxe',0)


def test_recipe_output_capacity_rollback(s):
    add(s,'oak_log',2304)
    s.command(AS + 'function npcraft:craft/recipes/oak_planks')
    count(s,'oak_log',2304)
    count(s,'oak_planks',0)


def test_station_required(s):
    add(s,'oak_planks',3);add(s,'stick',2)
    s.command(AS + 'function npcraft:craft/recipes/wooden_pickaxe')
    count(s,'wooden_pickaxe',0)
    table(s)
    s.command(AS + 'function npcraft:craft/recipes/wooden_pickaxe')
    count(s,'wooden_pickaxe',1)
    count(s,'oak_planks',0);count(s,'stick',0)


def test_station_reach_and_removal(s):
    table(s);add(s,'cobblestone',3);add(s,'stick',2)
    s.command(f'tp {BOT} 10.5 64 0.5')
    s.command(AS+'function npcraft:craft/recipes/stone_pickaxe')
    count(s,'stone_pickaxe',0)
    s.command(f'tp {BOT} 0.5 64 0.5')
    s.command('setblock 1 64 0 minecraft:air')
    s.command(AS+'function npcraft:craft/recipes/stone_pickaxe')
    count(s,'stone_pickaxe',0);count(s,'cobblestone',3)


def target(s, kind='oak_log', x=1,y=64,z=0):
    init(s)
    s.command(f'setblock {x} {y} {z} minecraft:{kind}')
    s.command(AS + f'data modify entity @s data.agent.target set value {{x:{x},y:{y},z:{z},kind:"minecraft:{kind}"}}')


def cut(s):
    s.command(f'scoreboard players set {BOT} np.dig 1')
    s.command(AS + 'function npcraft:action/mine')


def test_barehand_log(s):
    target(s);cut(s)
    s.expect('if block 1 64 0 minecraft:air');count(s,'oak_log',1)


def test_stone_requires_pick(s):
    target(s,'stone');cut(s)
    s.expect('if block 1 64 0 minecraft:stone');count(s,'cobblestone',0)
    add(s,'wooden_pickaxe',1,1)
    target(s,'stone');cut(s)
    s.expect('if block 1 64 0 minecraft:air');count(s,'cobblestone',1)
    s.expect(f'if data entity {BOT} data.agent.bag[0].item.components{{"minecraft:damage":1}}')


def test_mining_support_and_whitelist(s):
    target(s,'stone',x=0)
    s.command(f'tp {BOT} 0.5 65 0.5')
    s.command(AS+'function npcraft:bot/sync with entity @s data')
    add(s,'wooden_pickaxe',1,1);cut(s)
    s.expect('if block 0 64 0 minecraft:stone')
    s.command(f'tp {BOT} 0.5 64 2.5')
    target(s,'diamond_block');cut(s)
    s.expect('if block 1 64 0 minecraft:diamond_block')
    count(s,'diamond_block',0)


def test_action_bounds(s):
    target(s,x=4);cut(s)
    s.expect('if block 4 64 0 minecraft:oak_log');count(s,'oak_log',0)


def test_action_full_inventory(s):
    add(s,'cobblestone',2304);target(s);cut(s)
    s.expect('if block 1 64 0 minecraft:oak_log')
    count(s,'oak_log',0);count(s,'cobblestone',2304)


def test_inventory_tool_break(s):
    add(s,'wooden_pickaxe',1,1,components='{"minecraft:damage":58}')
    target(s,'stone');cut(s)
    count(s,'wooden_pickaxe',0);count(s,'cobblestone',1)


def test_step_up_down(s):
    s.command('fill 1 64 -1 3 64 1 minecraft:stone')
    s.command(AS+'data modify entity @s data.dest set value {x:3,y:65,z:0,range:0}')
    for _ in range(8):s.command(AS+'function npcraft:nav/plan')
    s.expect(f'if data entity {BOT} {{Pos:[3.5d,65.0d,0.5d]}}')
    s.command(AS+'data modify entity @s data.dest set value {x:5,y:64,z:0,range:0}')
    for _ in range(8):s.command(AS+'function npcraft:nav/plan')
    s.expect(f'if data entity {BOT} {{Pos:[5.5d,64.0d,0.5d]}}')


def test_low_ceiling_blocks_step(s):
    s.command('fill -1 64 -1 1 66 1 minecraft:stone hollow')
    s.command('setblock 0 64 0 minecraft:air')
    s.command('setblock 0 65 0 minecraft:air')
    s.command('setblock 1 65 0 minecraft:air')
    s.command('setblock 1 66 0 minecraft:air')
    s.command(AS+'data modify entity @s data.dest set value {x:1,y:65,z:0,range:0}')
    s.command(AS+'function npcraft:nav/plan')
    s.expect(f'if data entity {BOT} {{Pos:[0.5d,64.0d,0.5d]}}')


def test_step_revalidation(s):
    s.command('setblock 1 64 0 minecraft:stone')
    s.command('setblock 0 66 0 minecraft:stone')
    s.command(AS+'function npcraft:nav/move_macro {x:1.5,y:65.0,z:0.5}')
    s.expect(f'if data entity {BOT} {{Pos:[0.5d,64.0d,0.5d]}}')


def test_no_two_block_drop(s):
    s.command('fill 1 62 -8 2 63 8 minecraft:air')
    s.command('fill 1 61 -8 2 61 8 minecraft:stone')
    s.command(AS+'data modify entity @s data.dest set value {x:1,y:62,z:0,range:0}')
    s.command(AS+'function npcraft:nav/plan')
    s.expect(f'if data entity {BOT} {{Pos:[0.5d,64.0d,0.5d]}}')


def grove(s):
    init(s)
    s.command(f'tp {BOT} -0.5 64 3.5')
    s.command(AS+'function npcraft:bot/sync with entity @s data')
    s.command(AS+'data remove entity @s data.tool')
    for x,z in [(2,1),(2,-1)]:
        s.command(f'fill {x} 64 {z} {x} 67 {z} minecraft:oak_log')
    for x,z in [(3,z) for z in range(-3,4)]+[(-3,z) for z in range(-3,4)]+[(-2,-3),(-1,-3)]:
        s.command(f'setblock {x} 64 {z} minecraft:stone')


def drive(s, until, ticks=700):
    for i in range(ticks):
        s.command(f'scoreboard players set #now np.sys {1000+i*5}')
        s.command(AS+'function npcraft:agent/tick')
        s.command(AS+'function npcraft:bot/sync with entity @s data')
        if i%10==0:
            try:s.expect(until);return
            except AssertionError:pass
    s.expect(until)


def test_autonomous_stone_kit(s):
    grove(s)
    drive(s,f'if data entity {BOT} data.agent{{task:"stone_kit_ready"}}')
    for item in ('stone_pickaxe','stone_sword','stone_axe','furnace'):count(s,item,1)
    s.expect('if block 0 64 0 minecraft:crafting_table')
    s.expect(f'if data entity {BOT} data.agent{{mined:19}}')  # Three logs and 16 stone, no free ingredients.


def test_missing_resources_wait(s):
    init(s)
    drive(s,f'if data entity {BOT} data.agent{{task:"resource_unavailable_waiting"}}',40)
    count(s,'stone_pickaxe',0)
    s.expect('if score #nodes np.tmp matches ..128')


def test_stale_resource_replans(s):
    init(s);target(s)
    s.command('setblock 1 64 0 minecraft:air')
    s.command(AS+'function npcraft:agent/move_target with entity @s data.agent.target')
    s.expect(f'if data entity {BOT} data.agent.target',False)


def test_blacklist_bounded_and_expiring(s):
    init(s)
    for i in range(20):
        s.command(AS+f'data modify entity @s data.agent.target set value {{x:{i},y:64,z:0,kind:"minecraft:stone"}}')
        s.command(AS+'function npcraft:agent/blacklist')
    s.command(AS+'execute store result score #length np.tmp run data get entity @s data.agent.blocked')
    s.expect('if score #length np.tmp matches 16')
    s.command(AS+'function npcraft:agent/forget')
    s.expect(f'if data entity {BOT} data.agent.blocked[0]',False)


def test_backpack_dismissal(s):
    add(s,'oak_log',7);add(s,'stone_sword',1,1)
    s.command(AS+'function npcraft:inventory/drop_all')
    s.expect(f'if data entity {BOT} data.agent.bag[].item',False)
    s.command(AS+'function npcraft:inventory/drop_all')
    s.command('execute store result score #items np.tmp run execute if entity @e[type=minecraft:item]')
    s.expect('if score #items np.tmp matches 2')


def test_backpack_restart(s):
    add(s,'oak_log',70);add(s,'wooden_pickaxe',1,1,components='{"minecraft:damage":12}')
    s.command('save-all flush');s.stop();s.start()
    count(s,'oak_log',70);count(s,'wooden_pickaxe',1)
    s.expect(f'if data entity {BOT} data.agent.bag[2].item.components{{"minecraft:damage":12}}')


TESTS = [value for key,value in list(globals().items()) if key.startswith('test_') and callable(value)]
if __name__ == '__main__':
    base.TESTS = TESTS
    raise SystemExit(base.main())
