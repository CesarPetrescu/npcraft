"""Real vanilla regression cases for agent foundations; no simulated command engine."""
from __future__ import annotations
import json

BOT = '@e[type=minecraft:marker,tag=npcraft.test,limit=1]'
AS = f'execute as {BOT} at @s run '


def put(s, item, count=1, limit=64, components=None):
    stack = {'id': item, 'count': count}
    if components is not None:
        stack['components'] = components
    s.command(AS + 'function npcraft:inventory/load')
    s.command('data modify storage npcraft:inv input set value ' + json.dumps({'item': stack, 'max': limit}))
    s.command(AS + 'function npcraft:inventory/insert')
    s.expect('if score #inv_ok np.tmp matches 1')
    s.command(AS + 'function npcraft:inventory/commit')


def target(s, x=1, y=64, z=0, kind='stone'):
    s.command(f'setblock {x} {y} {z} minecraft:{kind}')
    s.command(AS + f'data modify entity @s data.target set value {{x:{x},y:{y},z:{z},kind:"minecraft:{kind}"}}')
    s.command(AS + 'function npcraft:agent/init')


def test_agent_inventory_component_merge(s):
    components = {'minecraft:custom_name': {'text': 'Kept name'}, 'minecraft:custom_data': {'serial': 7}}
    put(s, 'minecraft:diamond', 5, components=components)
    put(s, 'minecraft:diamond', 59, components=components)
    put(s, 'minecraft:diamond', 1, components=components)
    put(s, 'minecraft:diamond', 1, components={'minecraft:custom_name': {'text': 'Other name'}})
    s.expect(f'if data entity {BOT} data.inventory.slots[0].item{{count:64,components:{{"minecraft:custom_data":{{serial:7}}}}}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[1].item{{count:1}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[2].item.components{{"minecraft:custom_name":{{text:"Other name"}}}}')


def test_agent_inventory_capacity_rollback(s):
    s.command(AS + 'function npcraft:agent/init')
    slots = [{'item': {'id': 'minecraft:stone', 'count': 63 if i == 0 else 64}, 'max': 64} for i in range(36)]
    # Keep each fixture command below the vanilla RCON request buffer.
    for index, slot in enumerate(slots):
        s.command(AS + f'data modify entity @s data.inventory.slots[{index}] set value ' + json.dumps(slot))
    s.command(AS + 'function npcraft:inventory/load')
    s.command('data modify storage npcraft:inv input set value {item:{id:"minecraft:stone",count:2},max:64}')
    s.command(AS + 'function npcraft:inventory/insert')
    s.expect('if score #inv_ok np.tmp matches 0')
    s.expect(f'if data entity {BOT} data.inventory.slots[0].item{{count:63}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[35].item{{count:64}}')


def test_agent_inventory_stack_limits(s):
    put(s, 'minecraft:ender_pearl', 16, 16)
    put(s, 'minecraft:ender_pearl', 1, 16)
    put(s, 'minecraft:iron_sword', 1, 1, {'minecraft:damage': 8})
    s.expect(f'if data entity {BOT} data.inventory.slots[0].item{{count:16}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[1].item{{count:1}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[2].item.components{{"minecraft:damage":8}}')
    s.command(AS + 'function npcraft:inventory/load')
    s.command('data modify storage npcraft:inv input set value {item:{id:"minecraft:iron_sword",count:2},max:1}')
    s.command(AS + 'function npcraft:inventory/insert')
    s.expect('if score #inv_ok np.tmp matches 0')


def test_agent_recipe_atomicity(s):
    put(s, 'minecraft:oak_planks', 3)
    s.command(AS + 'function npcraft:actions/recipes/wood_pick')
    s.expect(f'if data entity {BOT} data.agent{{state:"blocked",reason:"missing_ingredients"}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[0].item{{id:"minecraft:oak_planks",count:3}}')
    put(s, 'minecraft:stick', 2)
    s.command(AS + 'function npcraft:actions/recipes/wood_pick')
    s.expect(f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:wooden_pickaxe",count:1}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:oak_planks"}}', False)
    s.expect(f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:stick"}}', False)


def test_agent_mixed_plank_recipe(s):
    put(s, 'minecraft:oak_planks', 1)
    put(s, 'minecraft:birch_planks', 1)
    s.command(AS + 'function npcraft:actions/recipes/sticks')
    s.expect(f'if data entity {BOT} data.inventory.slots[0].item{{id:"minecraft:stick",count:4}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[1].item', False)


def test_agent_missing_bench_rejected(s):
    put(s, 'minecraft:oak_planks', 3)
    put(s, 'minecraft:stick', 2)
    s.command(AS + 'data modify entity @s data.agent.intent set value "craft_wood_pick"')
    s.command(AS + 'function npcraft:actions/craft')
    s.expect(f'if data entity {BOT} data.agent{{reason:"assign_real_workbench"}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[0].item{{count:3}}')
    s.command(AS + 'data modify entity @s data.agent.bench set value {x:0,y:63,z:1}')
    s.command(AS + 'function npcraft:actions/craft')
    s.expect(f'if data entity {BOT} data.agent{{reason:"workbench_missing"}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[0].item{{count:3}}')


def test_agent_mining_requires_pick(s):
    target(s)
    s.command(AS + 'function npcraft:actions/mine_commit with entity @s data.target')
    s.expect('if block 1 64 0 minecraft:stone')
    s.expect(f'if data entity {BOT} data.agent{{reason:"need_plain_pickaxe"}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[].item', False)


def test_agent_mining_wear_and_drop(s):
    put(s, 'minecraft:wooden_pickaxe', 1, 1, {'minecraft:damage': 58})
    target(s)
    s.command(AS + 'function npcraft:actions/mine_commit with entity @s data.target')
    s.expect('if block 1 64 0 minecraft:air')
    s.expect(f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:cobblestone",count:1}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:wooden_pickaxe"}}', False)
    s.expect(f'if score {BOT} np.harvest matches 1')


def test_agent_mining_boundaries_and_reach(s):
    target(s, x=4, kind='oak_log')
    s.command(AS + 'function npcraft:actions/mine_commit with entity @s data.target')
    s.expect('if block 4 64 0 minecraft:oak_log')
    target(s, x=3, kind='oak_log')
    s.command(f'tp {BOT} -7.5 64 0.5')
    s.command(AS + 'function npcraft:actions/mine_commit with entity @s data.target')
    s.expect('if block 3 64 0 minecraft:oak_log')
    s.expect(f'if data entity {BOT} data.agent{{reason:"line_of_sight"}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[].item', False)


def test_agent_full_backpack_preserves_block(s):
    test_agent_inventory_capacity_rollback(s)
    target(s, kind='oak_log')
    s.command(AS + 'function npcraft:actions/mine_commit with entity @s data.target')
    s.expect('if block 1 64 0 minecraft:oak_log')
    s.expect(f'if data entity {BOT} data.agent{{reason:"backpack_full"}}')


def test_agent_vertical_ascent(s):
    s.command('fill 2 64 -1 4 64 1 minecraft:stone')
    s.command(AS + 'data modify entity @s data.dest set value {x:3,y:65,z:0,range:0}')
    for _ in range(12):
        s.command(AS + 'function npcraft:nav/plan')
    s.expect(f'if data entity {BOT} {{Pos:[3.5d,65.0d,0.5d]}}')
    s.expect('if block 2 64 0 minecraft:stone')
    s.expect('if entity @e[tag=npcraft.nav]', False)


def test_agent_safe_drop_two(s):
    s.command('fill 0 64 0 0 65 0 minecraft:stone')
    s.command(f'tp {BOT} 0.5 66 0.5')
    s.command(AS + 'data modify entity @s data.dest set value {x:1,y:64,z:0,range:0}')
    for _ in range(4):
        s.command(AS + 'function npcraft:nav/plan')
    s.expect(f'if data entity {BOT} {{Pos:[1.5d,64.0d,0.5d]}}')


def test_agent_unsafe_drop_three(s):
    s.command('fill 0 64 0 0 66 0 minecraft:stone')
    s.command(f'tp {BOT} 0.5 67 0.5')
    s.command(AS + 'data modify entity @s data.dest set value {x:1,y:64,z:0,range:0}')
    s.command(AS + 'function npcraft:nav/plan')
    s.expect(f'if data entity {BOT} {{Pos:[0.5d,67.0d,0.5d]}}')


def test_agent_head_sweep_revalidation(s):
    s.command('setblock 1 64 0 minecraft:stone')
    s.command('setblock 0 66 0 minecraft:stone')
    s.command(AS + 'data modify entity @s data.dest set value {x:1,y:65,z:0,range:0}')
    s.command(AS + 'execute store result score #sweep np.tmp run function npcraft:nav/step_safe {x:1.5d,y:65.0d,z:0.5d}')
    s.expect('if score #sweep np.tmp matches 0')
    s.command('setblock 0 66 0 minecraft:air')
    s.command(AS + 'execute store result score #sweep np.tmp run function npcraft:nav/step_safe {x:1.5d,y:65.0d,z:0.5d}')
    s.expect('if score #sweep np.tmp matches 1')
    s.command('setblock 1 64 0 minecraft:air')
    s.command(AS + 'execute store result score #sweep np.tmp run function npcraft:nav/step_safe {x:1.5d,y:65.0d,z:0.5d}')
    s.expect('if score #sweep np.tmp matches 0')


def test_agent_failed_target_memory(s):
    target(s, kind='oak_log')
    for _ in range(3):
        s.command(AS + 'function npcraft:agent/failure')
    s.expect(f'if data entity {BOT} data.agent.blocked[{{x:1,y:64,z:0}}]')
    s.expect(f'if data entity {BOT} data.target', False)
    s.command(AS + 'data modify entity @s data.agent.intent set value "gather_logs"')
    s.command(AS + 'function npcraft:agent/candidate {x:1,y:64,z:0}')
    s.expect(f'if data entity {BOT} data.target', False)


def test_agent_no_owner_no_progress(s):
    target(s, kind='oak_log')
    s.command(AS + 'function npcraft:agent/start')
    s.command(AS + 'function npcraft:bot/brain with entity @s data')
    s.expect('if block 1 64 0 minecraft:oak_log')
    s.expect(f'if data entity {BOT} data.inventory.slots[].item', False)


def test_agent_backpack_persists(s):
    put(s, 'minecraft:diamond', 19, components={'minecraft:custom_data': {'token': 42}})
    s.command('save-all flush')
    s.stop()
    s.start()
    s.expect(f'if data entity {BOT} data.inventory.slots[0].item{{count:19,components:{{"minecraft:custom_data":{{token:42}}}}}}')


def test_agent_goal_end_to_end(s):
    s.command(AS + 'function npcraft:agent/start')
    s.command(AS + 'data remove entity @s data.tool')
    s.command('setblock 0 63 1 minecraft:crafting_table')
    s.command(AS + 'data modify entity @s data.agent.bench set value {x:0,y:63,z:1}')
    for x, z in [(-1, 0), (1, 0)]:
        s.command(f'setblock {x} 64 {z} minecraft:oak_log')
    for x, z in [(-2, -1), (2, -1), (0, -2)]:
        s.command(f'setblock {x} 64 {z} minecraft:stone')
    for _ in range(250):
        s.command('scoreboard players add #now np.sys 10')
        s.command(AS + 'function npcraft:agent/tick')
        if 'stone_pickaxe_obtained' in s.command(f'data get entity {BOT} data.agent.reason'):
            break
    else:
        raise AssertionError('Goal did not complete: ' + s.command(f'data get entity {BOT} data'))
    s.expect(f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:stone_pickaxe",count:1}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:wooden_pickaxe",components:{{"minecraft:damage":3}}}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:oak_planks",count:3}}')
    s.expect(f'if score {BOT} np.harvest matches 5')
    s.expect(f'if data entity {BOT} data.inventory.slots[].item{{id:"minecraft:cobblestone"}}', False)
    # No repeat crafting or mining after success.
    for _ in range(5):
        s.command(AS + 'function npcraft:agent/tick')
    s.expect(f'if score {BOT} np.harvest matches 5')


def test_agent_read_only_and_unknown_commands(s):
    target(s, kind='oak_log')
    s.command(f'scoreboard players set {BOT} np.dig 12345')
    s.command(f'scoreboard players set {BOT} np.mode 4')
    for action in (13, 20, 25, 19, 26, 98):
        s.command(f'scoreboard players set #cmd np.tmp {action}')
        s.command(AS + 'function npcraft:commands/owned')
        s.expect(f'if data entity {BOT} data.target{{x:1,y:64,z:0}}')
        s.expect(f'if score {BOT} np.dig matches 12345')
        s.expect(f'if score {BOT} np.mode matches 4')


def test_agent_additive_initialization_preserves_legacy(s):
    before = s.command(f'data get entity {BOT} data.tool')
    s.command(AS + 'data modify entity @s data.cargo set value {id:"minecraft:oak_log",count:31}')
    for _ in range(3):
        s.command(AS + 'function npcraft:agent/init')
    s.expect(f'if data entity {BOT} data.cargo{{count:31}}')
    s.expect(f'if data entity {BOT} data{{owner_uuid:[I;0,0,0,1]}}')
    if before != s.command(f'data get entity {BOT} data.tool'):
        raise AssertionError('Agent initialization changed the legacy tool')
    put(s, 'minecraft:diamond', 3)
    s.command(AS + 'function npcraft:agent/init')
    s.expect(f'if data entity {BOT} data.inventory.slots[0].item{{count:3}}')


AGENT_TESTS = [value for name, value in sorted(globals().items()) if name.startswith('test_agent_')]
