"""Additional real-server disruption, contention and persistence fixtures."""
import time
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from tools.agent_tests import BOT, AS, put, target
from tools.v03_tests import furnace_fixture, count


def test_v03_interrupted_furnace_preserves_foreign_items(s):
    furnace_fixture(s)
    put(s,'minecraft:raw_iron',2)
    put(s,'minecraft:coal',2)
    s.command('item replace block 1 64 0 container.0 with minecraft:diamond 9')
    s.command(AS+'function npcraft:stations/operate with entity @s data.agent.furnace')
    s.expect(f'if data entity {BOT} data.agent{{reason:"foreign_furnace_input"}}')
    assert count(s,'minecraft:raw_iron')==2
    s.expect('if data block 1 64 0 Items[{Slot:0b,id:"minecraft:diamond",count:9}]')
    s.command('item replace block 1 64 0 container.0 with minecraft:air')
    s.command('item replace block 1 64 0 container.1 with minecraft:diamond 8')
    s.command(AS+'function npcraft:stations/operate with entity @s data.agent.furnace')
    s.expect(f'if data entity {BOT} data.agent{{reason:"foreign_furnace_fuel"}}')
    assert count(s,'minecraft:coal')==2


def test_v03_furnace_consumes_no_input_without_capacity(s):
    furnace_fixture(s)
    # Existing real furnace output stays put while backpack is full.
    for i in range(36):
        s.command(AS+f'data modify entity @s data.inventory.slots[{i}] set value {{item:{{id:"minecraft:cobblestone",count:64}},max:64}}')
    s.command('item replace block 1 64 0 container.2 with minecraft:iron_ingot 7')
    for _ in range(4):s.command(AS+'function npcraft:stations/operate with entity @s data.agent.furnace')
    s.expect('if data block 1 64 0 Items[{Slot:2b,id:"minecraft:iron_ingot",count:7}]')
    s.command(AS+'data modify entity @s data.inventory.slots[35] set value {}')
    s.command(AS+'function npcraft:stations/operate with entity @s data.agent.furnace')
    assert count(s,'minecraft:iron_ingot')==7
    s.expect('if data block 1 64 0 Items[{Slot:2b}]',False)


def test_v03_two_agents_cannot_duplicate_one_ore(s):
    put(s,'minecraft:stone_pickaxe',1,1)
    target(s,kind='iron_ore')
    other='@e[type=minecraft:marker,tag=npcraft.contender,limit=1]'
    s.command('summon minecraft:marker 0.5 64 1.5 {Tags:["npcraft.bot","npcraft.contender"]}')
    s.command(f'data modify entity {other} data set from entity {BOT} data')
    s.command(f'data modify entity {other} data.id set value 9002')
    s.command(f'scoreboard players set {other} np.id 9002')
    s.command(f'scoreboard players set {other} np.harvest 0')
    s.command(AS+'function npcraft:actions/mine_commit with entity @s data.target')
    s.command(f'execute as {other} at @s run function npcraft:actions/mine_commit with entity @s data.target')
    assert count(s,'minecraft:raw_iron')==1
    s.expect(f'if data entity {other} data.inventory.slots[].item{{id:"minecraft:raw_iron"}}',False)
    s.expect(f'if score {other} np.harvest matches 0')
    s.expect('if block 1 64 0 minecraft:air')


def test_v03_no_food_means_no_healing(s):
    s.command(AS+'function npcraft:survival/enable')
    s.command('damage @e[type=minecraft:mannequin,tag=npcraft.body,limit=1] 8 minecraft:generic')
    s.command(AS+'data modify entity @s data.survival.food set value 4')
    for _ in range(3):s.command(AS+'function npcraft:survival/eat with entity @s data')
    s.expect('if data entity @e[type=minecraft:mannequin,tag=npcraft.body,limit=1] {Health:12.0f}')
    s.expect(f'if data entity {BOT} data.survival{{food:4}}')


def test_v03_death_record_survives_restart(s):
    put(s,'minecraft:diamond',5)
    s.command(AS+'function npcraft:survival/enable')
    s.command('damage @e[type=minecraft:mannequin,tag=npcraft.body,limit=1] 100 minecraft:generic')
    s.command(AS+'function npcraft:survival/tick with entity @s data')
    time.sleep(.15)
    s.command('function npcraft:runtime/tick')
    s.expect(f'if data entity {BOT} data.survival{{dead:1b,deaths:1}}')
    s.command('save-all flush');s.stop();s.start()
    s.expect(f'if data entity {BOT} data.survival{{dead:1b,deaths:1}}')
    assert count(s,'minecraft:diamond')==0
    s.expect('if entity @e[type=minecraft:item,tag=npcraft.loot,nbt={Item:{id:"minecraft:diamond",count:5}}]')
    s.command(AS+'function npcraft:survival/dead_tick')
    s.command('execute store result score #loot_count np.tmp run execute if entity @e[type=minecraft:item,nbt={Item:{id:"minecraft:diamond"}}]')
    s.expect('if score #loot_count np.tmp matches 1')


def test_v03_rival_permission_revocation_is_persistent(s):
    s.command('data modify storage npcraft:state acl set value [{id:1,allowed:0b}]')
    s.command('data modify storage npcraft:state consents set value [{id:1,token:101}]')
    s.command(AS+'data modify entity @s data.rival set value {enabled:1b,token:101}')
    s.command(AS+'execute store result score #access np.tmp run function npcraft:rival/access')
    s.expect('if score #access np.tmp matches 0')
    s.command('reload');time.sleep(1)
    s.command(AS+'execute store result score #access np.tmp run function npcraft:rival/access')
    s.expect('if score #access np.tmp matches 0')


def test_v03_legacy_and_backpack_survive_additive_upgrade(s):
    put(s,'minecraft:diamond',3)
    s.command(AS+'data modify entity @s data.cargo set value {id:"minecraft:oak_log",count:18}')
    for _ in range(3):s.command(AS+'function npcraft:agent/init')
    s.expect(f'if data entity {BOT} data.tool{{id:"minecraft:iron_axe"}}')
    s.expect(f'if data entity {BOT} data.cargo{{id:"minecraft:oak_log",count:18}}')
    assert count(s,'minecraft:diamond')==3


ADVERSARIAL_TESTS=[v for k,v in sorted(globals().items()) if k.startswith('test_v03_')]

if __name__=="__main__":
    from tools import server_test
    server_test.TESTS=ADVERSARIAL_TESTS
    raise SystemExit(server_test.main())
