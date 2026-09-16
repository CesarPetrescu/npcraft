"""Real Minecraft regressions for lifecycle, cached routes, and consent boundaries."""
from __future__ import annotations
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.agent_tests import BOT, AS, put
from tools.v03_tests import count


def test_acl_round_trip_preserves_boolean_nbt(s):
    # Macro expansion removes numeric type suffixes; writing the byte back matters.
    s.command('function npcraft:rival/acl_write {id:1,allowed:1b}')
    s.command('function npcraft:rival/consent_write {id:1,token:77}')
    s.command(AS+'data modify entity @s data.rival set value {enabled:1b,token:77}')
    s.expect('if data storage npcraft:state acl[{id:1,allowed:1b}]')
    s.command(AS+'execute store result score #access np.tmp run function npcraft:rival/access')
    s.expect('if score #access np.tmp matches 1')
    s.command('function npcraft:rival/acl_write {id:1,allowed:0b}')
    s.command(AS+'execute store result score #access np.tmp run function npcraft:rival/access')
    s.expect('if score #access np.tmp matches 0')
    s.command('reload');time.sleep(.5)
    s.expect('if data storage npcraft:state acl[{id:1,allowed:0b}]')


def test_mortal_body_stays_alive_with_primed_death_timer(s):
    s.command(AS+'function npcraft:survival/enable')
    time.sleep(.5)
    s.expect('if entity @e[type=minecraft:mannequin,tag=npcraft.body]')
    s.expect('if data entity @e[type=minecraft:mannequin,tag=npcraft.body,limit=1] {Health:20.0f}')
    s.command('damage @e[type=minecraft:mannequin,tag=npcraft.body,limit=1] 3 minecraft:generic')
    s.expect('if data entity @e[type=minecraft:mannequin,tag=npcraft.body,limit=1] {Health:17.0f}')
    s.command('save-all flush')
    s.assert_clean_logs()


def test_cached_route_invalidates_after_new_obstruction(s):
    s.command(AS+'data modify entity @s data.dest set value {x:5,y:64,z:0,range:0}')
    s.command(AS+'function npcraft:nav/plan')
    s.expect(f'if data entity {BOT} data.navigation.steps[0]')
    s.command(AS+'data modify storage npcraft:qa step.p set from entity @s data.navigation.steps[0]')
    for axis,index in [('x',0),('y',1),('z',2)]:
        s.command(f'execute store result storage npcraft:qa step.{axis} int 1 run data get storage npcraft:qa step.p[{index}]')
    s.command('function npcraft:qa/block_step with storage npcraft:qa step')
    s.command(AS+'data modify storage npcraft:qa before set from entity @s Pos')
    s.command(AS+'function npcraft:nav/advance')
    s.command(AS+'data modify storage npcraft:qa after set from entity @s Pos')
    s.command('execute store success score #changed np.tmp run data modify storage npcraft:qa after set from storage npcraft:qa before')
    s.expect('if score #changed np.tmp matches 0')
    s.expect(f'if data entity {BOT} data.navigation',False)


def test_broken_iron_pick_does_not_satisfy_readiness(s):
    put(s,'minecraft:iron_pickaxe',1,1,{'minecraft:damage':250})
    s.command(AS+'function npcraft:inventory/load')
    s.command(AS+'function npcraft:agent/observe')
    s.expect('if score #pick_best np.tmp matches 0')
    s.command(AS+'function npcraft:progression/observe')
    s.expect('if score #pg_pick np.tmp matches 0')


def test_dropped_food_cannot_heal_dead_controller(s):
    put(s,'minecraft:bread',2)
    s.command(AS+'function npcraft:survival/enable')
    s.command('tick freeze')
    try:
        s.command(AS+'data modify entity @s data.survival.dead set value 1b')
        s.command(AS+'function npcraft:survival/eat with entity @s data')
        assert count(s,'minecraft:bread')==2, 'Dead controller consumed food'
    finally:
        s.command('tick unfreeze')


def test_respawn_never_duplicates_marked_loot(s):
    put(s,'minecraft:diamond',9,components={'minecraft:custom_data':{'check':77}})
    s.command(AS+'function npcraft:survival/enable')
    s.command('damage @e[type=minecraft:mannequin,tag=npcraft.body,limit=1] 100 minecraft:generic')
    s.command(AS+'function npcraft:survival/tick with entity @s data')
    time.sleep(.15)
    s.command(AS+'function npcraft:survival/respawn with entity @s data.home')
    for _ in range(4):s.command(AS+'function npcraft:survival/pickup with entity @s data')
    assert count(s,'minecraft:diamond')==9
    s.expect('if entity @e[type=minecraft:item,nbt={Item:{id:"minecraft:diamond"}}]',False)
    s.command('save-all flush');s.stop();s.start()
    assert count(s,'minecraft:diamond')==9


# Fixture-only block mutation is installed into a disposable secondary datapack.
def install_test_helper(server):
    import json
    root=server.work/'world/datapacks/npcraft-reliability-qa'
    f=root/'data/npcraft/function/qa/block_step.mcfunction';f.parent.mkdir(parents=True,exist_ok=True)
    (root/'pack.mcmeta').write_text(json.dumps({'pack':{'description':'Disposable test helper','min_format':[121,0],'max_format':[121,0]}}))
    f.write_text('$setblock $(x) $(y) $(z) minecraft:stone\n')
    server.command('reload');time.sleep(.5)


def main():
    from tools import server_test
    previous_fixture=server_test.fixture
    def fixture(s):
        previous_fixture(s)
        if not (s.work/'world/datapacks/npcraft-reliability-qa').exists():install_test_helper(s)
    server_test.fixture=fixture
    server_test.TESTS=[v for k,v in sorted(globals().items()) if k.startswith('test_')]
    return server_test.main()


if __name__=='__main__':raise SystemExit(main())
