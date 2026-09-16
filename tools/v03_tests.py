"""Real-server progression and adversarial regression cases, not a simulated world."""
from __future__ import annotations
import json
import time
from tools.agent_tests import BOT, AS, put, target


def count(s, item):
    s.command(AS + 'function npcraft:inventory/load')
    s.command(AS + 'function npcraft:inventory/count ' + json.dumps({'kind':item}))
    answer=s.command('scoreboard players get #iv_total np.tmp')
    import re
    return int(re.search(r'has (-?\d+)',answer).group(1))


def test_v03_named_pick_is_usable(s):
    put(s,'minecraft:stone_pickaxe',1,1,{'minecraft:damage':4,'minecraft:custom_name':{'text':'Mine'}})
    s.command(AS+'function npcraft:inventory/load')
    s.command(AS+'function npcraft:agent/observe')
    s.expect('if score #ag_stone_pick np.tmp matches 1')
    target(s)
    s.command(AS+'function npcraft:actions/mine_commit with entity @s data.target')
    s.expect(f'if data entity {BOT} data.inventory.slots[].item{{components:{{"minecraft:damage":5,"minecraft:custom_name":{{text:"Mine"}}}}}}')


def test_v03_unusable_stone_does_not_complete_goal(s):
    put(s,'minecraft:stone_pickaxe',1,1,{'minecraft:unbreakable':{}})
    s.command(AS+'function npcraft:inventory/load')
    s.command(AS+'function npcraft:agent/observe')
    s.command(AS+'function npcraft:agent/plan')
    s.expect('if score #ag_stone_pick np.tmp matches 0')
    s.expect(f'if data entity {BOT} data.agent{{intent:"complete"}}',False)


def test_v03_iron_tier_required(s):
    put(s,'minecraft:wooden_pickaxe',1,1)
    target(s,kind='iron_ore')
    s.command(AS+'function npcraft:actions/mine_commit with entity @s data.target')
    s.expect('if block 1 64 0 minecraft:iron_ore')
    s.expect(f'if data entity {BOT} data.agent{{reason:"need_stone_tier"}}')
    put(s,'minecraft:stone_pickaxe',1,1)
    s.command(AS+'function npcraft:actions/mine_commit with entity @s data.target')
    s.expect('if block 1 64 0 minecraft:air')
    assert count(s,'minecraft:raw_iron')==1


def test_v03_station_consumption_and_collision(s):
    put(s,'minecraft:crafting_table',1)
    s.command(AS+'function npcraft:stations/place {kind:"minecraft:crafting_table",key:"bench"}')
    s.expect(f'if data entity {BOT} data.agent.bench{{owned:1b}}')
    assert count(s,'minecraft:crafting_table')==0
    # Attempt another placement without an item must not grant a free station.
    s.command(AS+'function npcraft:stations/place {kind:"minecraft:furnace",key:"furnace"}')
    s.expect(f'if data entity {BOT} data.agent.furnace',False)
    for x,z in [(1,0),(-1,0),(0,1),(0,-1)]:
        s.command(f'setblock {x} 64 {z} minecraft:stone')
    put(s,'minecraft:furnace',1)
    s.command(AS+'function npcraft:stations/place {kind:"minecraft:furnace",key:"furnace"}')
    assert count(s,'minecraft:furnace')==1
    s.expect('if block 1 64 0 minecraft:stone')


def furnace_fixture(s):
    put(s,'minecraft:furnace',1)
    s.command(AS+'function npcraft:stations/place {kind:"minecraft:furnace",key:"furnace"}')
    s.expect(f'if data entity {BOT} data.agent.furnace{{x:1,y:64,z:0}}')


def test_v03_replaced_furnace_not_looted(s):
    furnace_fixture(s)
    s.command('setblock 1 64 0 minecraft:air')
    s.command('setblock 1 64 0 minecraft:furnace')
    s.command('item replace block 1 64 0 container.2 with minecraft:iron_ingot 12')
    s.command(AS+'function npcraft:stations/operate with entity @s data.agent.furnace')
    s.expect('if data block 1 64 0 Items[{Slot:2b,count:12}]')
    assert count(s,'minecraft:iron_ingot')==0


def test_v03_furnace_no_early_output_and_conservation(s):
    furnace_fixture(s)
    put(s,'minecraft:raw_iron',1)
    put(s,'minecraft:coal',1)
    s.command('tick freeze')
    try:
        s.command(AS+'function npcraft:progression/tick') # no plot prepared? original fixture has plot; may select another intent
        s.command(AS+'function npcraft:stations/operate with entity @s data.agent.furnace')
        s.expect('if data block 1 64 0 Items[{Slot:0b,id:"minecraft:raw_iron",count:1}]')
        s.expect('if data block 1 64 0 Items[{Slot:1b,id:"minecraft:coal",count:1}]')
        assert count(s,'minecraft:raw_iron')==0
        assert count(s,'minecraft:coal')==0
        assert count(s,'minecraft:iron_ingot')==0
    finally:
        s.command('tick unfreeze')
    deadline=time.monotonic()+20
    while time.monotonic()<deadline:
        if 'iron_ingot' in s.command('data get block 1 64 0 Items'):
            break
        time.sleep(.3)
    else:raise AssertionError('Native furnace did not produce iron')
    s.command(AS+'function npcraft:stations/operate with entity @s data.agent.furnace')
    assert count(s,'minecraft:iron_ingot')==1
    s.expect('if data block 1 64 0 Items[{Slot:2b}]',False)
    s.command(AS+'function npcraft:stations/operate with entity @s data.agent.furnace')
    assert count(s,'minecraft:iron_ingot')==1


def test_v03_furnace_capacity_preserves_output(s):
    furnace_fixture(s)
    for i in range(36):
        s.command(AS+f'data modify entity @s data.inventory.slots[{i}] set value {{item:{{id:"minecraft:stone",count:64}},max:64}}')
    s.command('item replace block 1 64 0 container.2 with minecraft:iron_ingot 3')
    s.command(AS+'function npcraft:stations/operate with entity @s data.agent.furnace')
    s.expect('if data block 1 64 0 Items[{Slot:2b,count:3}]')
    assert count(s,'minecraft:iron_ingot')==0


def iron_resources(s):
    # Open test lanes. All resources declared in the work plot. No prebuilt station or item grants.
    s.command(AS+'data remove entity @s data.tool')
    for x in (-3,3):
        s.command(f'fill {x} 64 -3 {x} 67 -3 minecraft:oak_log')
    for x,z in [(-3,-1),(-3,1),(-3,3),(3,-1),(3,1),(3,3)]:
        s.command(f'fill {x} 64 {z} {x} 67 {z} minecraft:stone')
    for x in (-2,0,2):s.command(f'setblock {x} 64 -3 minecraft:iron_ore')
    s.command('setblock 0 64 3 minecraft:coal_ore')


def test_v03_empty_to_iron_end_to_end(s):
    iron_resources(s)
    s.command(AS+'function npcraft:progression/start')
    deadline=time.monotonic()+100
    trace=set()
    while time.monotonic()<deadline:
        s.command('execute store result score #now np.sys run time query gametime')
        s.command(AS+'function npcraft:progression/tick')
        state=s.command(f'data get entity {BOT} data.agent')
        trace.add(s.command(f'data get entity {BOT} data.agent.intent'))
        if 'iron_pickaxe_obtained' in state:break
        time.sleep(.06)
    else:raise AssertionError('Iron progression failed: '+s.command(f'data get entity {BOT} data')+'\n'+str(sorted(trace)))
    assert count(s,'minecraft:iron_pickaxe')==1
    assert count(s,'minecraft:raw_iron')==0
    assert count(s,'minecraft:iron_ingot')==0
    assert count(s,'minecraft:stone_pickaxe')==1
    s.expect(f'if data entity {BOT} data.agent.bench{{owned:1b}}')
    s.expect(f'if data entity {BOT} data.agent.furnace{{owned:1b}}')
    # Supporting world resources, not invented inventory.
    for x in (-2,0,2):s.expect(f'if block {x} 64 -3 minecraft:air')
    before=s.command(f'scoreboard players get {BOT} np.harvest')
    for _ in range(5):s.command(AS+'function npcraft:progression/tick')
    assert before==s.command(f'scoreboard players get {BOT} np.harvest')

V03_TESTS=[v for k,v in sorted(globals().items()) if k.startswith('test_v03_')]


def test_v03_uuid_encoding_signed_words(s):
    s.command('data modify storage npcraft:uuid parts set value [I;-1,-2147483648,2147483647,1]')
    s.command('function npcraft:identity/encode')
    s.expect('if data storage npcraft:uuid {result:"ffffffff-8000-0000-7fff-ffff00000001"}')


def test_v03_mortality_and_food_transaction(s):
    s.command(AS+'function npcraft:survival/enable')
    put(s,'minecraft:bread',2)
    s.command('damage @e[type=minecraft:mannequin,tag=npcraft.body,limit=1] 5 minecraft:generic')
    s.command(AS+'data modify entity @s data.survival.food set value 10')
    s.command(AS+'function npcraft:survival/eat with entity @s data')
    assert count(s,'minecraft:bread')==1
    s.expect('if data entity @e[type=minecraft:mannequin,tag=npcraft.body,limit=1] {Health:17.0f}')
    s.expect(f'if data entity {BOT} data.survival{{food:15}}')
    s.command(AS+'function npcraft:survival/eat with entity @s data')
    assert count(s,'minecraft:bread')==1 # meal cooldown, no per-update infinite eating


def test_v03_death_drops_once_and_respawns_empty(s):
    put(s,'minecraft:diamond',7,components={'minecraft:custom_data':{'serial':91}})
    s.command(AS+'function npcraft:survival/enable')
    s.command('damage @e[type=minecraft:mannequin,tag=npcraft.body,limit=1] 100 minecraft:generic')
    s.command(AS+'function npcraft:survival/tick with entity @s data')
    s.expect(f'if data entity {BOT} data.survival{{dead:1b,deaths:1}}')
    s.expect(f'if data entity {BOT} data.inventory.slots[].item',False)
    time.sleep(.15)
    s.command('function npcraft:runtime/tick')
    s.expect('if entity @e[type=minecraft:item,nbt={Item:{id:"minecraft:diamond",count:7}}]')
    # The fixture also had one real legacy iron axe. The visual copy may NEVER be returned.
    s.command('execute store result score #drop_count np.tmp run execute if entity @e[type=minecraft:item]')
    s.expect('if score #drop_count np.tmp matches 2')
    for _ in range(3):s.command(AS+'function npcraft:survival/dead_tick')
    s.command('execute store result score #drop_count np.tmp run execute if entity @e[type=minecraft:item]')
    s.expect('if score #drop_count np.tmp matches 2')
    s.command('save-all flush')
    s.command(AS+'function npcraft:survival/respawn with entity @s data.home')
    s.expect(f'if data entity {BOT} data.survival{{dead:0b}}')
    s.expect('if entity @e[type=minecraft:mannequin,tag=npcraft.body]')
    assert count(s,'minecraft:diamond')==0
    s.command(AS+'function npcraft:survival/pickup with entity @s data')
    s.command(AS+'function npcraft:survival/pickup with entity @s data')
    assert count(s,'minecraft:diamond')==7
    s.expect(f'if data entity {BOT} data.inventory.slots[].item{{components:{{"minecraft:custom_data":{{serial:91}}}}}}')
    s.command('save-all flush')


def test_v03_unsafe_respawn_preserves_tombstone(s):
    s.command(AS+'function npcraft:survival/enable')
    s.command(AS+'data modify entity @s data.survival.dead set value 1b')
    s.command('setblock 0 64 0 minecraft:stone')
    s.command(AS+'function npcraft:survival/respawn with entity @s data.home')
    s.expect(f'if data entity {BOT} data.survival{{dead:1b}}')
    s.expect('if block 0 64 0 minecraft:stone')


def test_v03_consent_epoch_and_revoke(s):
    s.command('data modify storage npcraft:state acl set value [{id:1,allowed:1b}]')
    s.command('data modify storage npcraft:state consents set value [{id:1,token:100}]')
    s.command(AS+'data modify entity @s data.rival set value {enabled:1b,token:100,center:{x:0,y:64,z:0}}')
    s.command(AS+'execute store result score #access np.tmp run function npcraft:rival/access')
    s.expect('if score #access np.tmp matches 1')
    s.command('function npcraft:rival/revoke_consent {id:1}')
    s.command(AS+'execute store result score #access np.tmp run function npcraft:rival/access')
    s.expect('if score #access np.tmp matches 0')
    # A fresh consent token never silently re-enables an old unloaded opponent.
    s.command('function npcraft:rival/consent_write {id:1,token:101}')
    s.command(AS+'execute store result score #access np.tmp run function npcraft:rival/access')
    s.expect('if score #access np.tmp matches 0')


def test_v03_rival_cannot_step_outside_arena(s):
    s.command(AS+'data modify entity @s data.rival set value {enabled:1b,center:{x:0,y:64,z:0}}')
    s.command(AS+'execute store result score #arena np.tmp run function npcraft:rival/step_allowed {x:16.5,y:64.0,z:0.5}')
    s.expect('if score #arena np.tmp matches 1')
    s.command(AS+'execute store result score #arena np.tmp run function npcraft:rival/step_allowed {x:17.5,y:64.0,z:0.5}')
    s.expect('if score #arena np.tmp matches 0')


def test_v03_cache_reused_and_invalidated(s):
    s.command(AS+'function npcraft:nav/plan')
    s.expect(f'if data entity {BOT} data.navigation.steps[0]')
    s.command(AS+'function npcraft:nav/plan')
    s.expect('if score #nodes np.tmp matches 0') # real cache hit, no fresh BFS
    s.expect(f'if data entity {BOT} {{Pos:[2.5d,64.0d,0.5d]}}')
    s.command('fill 3 64 -8 3 69 8 minecraft:stone')
    s.command(AS+'function npcraft:nav/advance')
    s.expect(f'if data entity {BOT} {{Pos:[2.5d,64.0d,0.5d]}}')
    s.expect(f'if data entity {BOT} data.navigation',False)


V03_TESTS=[v for k,v in sorted(globals().items()) if k.startswith('test_v03_')]
