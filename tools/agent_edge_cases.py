"""Fail-closed and recovery cases for the actual-vanilla agent suite."""
from tools.agent_test import init, add, count, target, cut, grove, drive, BOT, AS


def test_unknown_inventory_schema(s):
    add(s,'oak_log',7)
    s.command(AS+'data modify entity @s data.agent.schema set value 99')
    add(s,'oak_log',2)
    s.expect('if score #iv_ok np.tmp matches 0')
    count(s,'oak_log',7)
    s.expect(f'if data entity {BOT} data.agent{{schema:99}}')


def test_invalid_inventory_length(s):
    init(s)
    s.command(AS+'data modify entity @s data.agent.bag set value []')
    add(s,'oak_log',1)
    s.expect('if score #iv_ok np.tmp matches 0')
    s.expect(f'if data entity {BOT} data.agent.bag[].item',False)


def test_unsupported_pick_not_used(s):
    add(s,'wooden_pickaxe',1,1,components='{"minecraft:unbreakable":{}}')
    target(s,'stone');cut(s)
    s.expect('if block 1 64 0 minecraft:stone')
    count(s,'cobblestone',0)
    count(s,'wooden_pickaxe',1)


def test_nonadjacent_move_rejected(s):
    s.command(AS+'function npcraft:nav/move_macro {x:6.5,y:64.0,z:0.5}')
    s.expect(f'if data entity {BOT} {{Pos:[0.5d,64.0d,0.5d]}}')


def test_blocked_workbench_retains_item(s):
    add(s,'crafting_table',1)
    s.command('setblock 0 64 0 minecraft:gold_block')
    s.command(AS+'function npcraft:craft/place_station')
    s.expect('if block 0 64 0 minecraft:gold_block')
    count(s,'crafting_table',1)
    s.expect(f'if data entity {BOT} data.agent{{task:"clear_plot_center_for_workbench"}}')


def test_replans_lost_sword(s):
    grove(s)
    drive(s,f'if data entity {BOT} data.agent{{task:"stone_kit_ready"}}')
    s.command(AS+'data modify entity @s data.agent.bag[{item:{id:"minecraft:stone_sword"}}] set value {}')
    s.command('setblock -3 64 -3 minecraft:stone')
    s.command('setblock -2 64 -3 minecraft:stone')
    drive(s,f'if data entity {BOT} data.agent.bag[{{item:{{id:"minecraft:stone_sword"}}}}]',200)
    count(s,'stone_sword',1)
    s.expect(f'if data entity {BOT} data.agent{{mined:21}}')


TESTS=[value for name,value in list(globals().items()) if name.startswith('test_') and callable(value)]
