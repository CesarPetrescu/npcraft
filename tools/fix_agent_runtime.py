"""Apply observed vanilla regressions to the canonical generator; temporary bootstrap."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'tools/generate_agent.py'
s=p.read_text()
s=s.replace('execute unless function npcraft:action/check with entity @s data.agent.target run', 'execute unless function npcraft:action/valid run')
if "fn('action/valid'" not in s:
    s=s.replace("    fn('action/mine',", "    fn('action/valid', 'return run function npcraft:action/check with entity @s data.agent.target')\n    fn('action/mine',")
p.write_text(s)
# Staged operations must never publish scratch belonging to an unsupported schema.
s=p.read_text()
if '#iv_ready' not in s:
    s=s.replace("    fn('inventory/begin', '''\n        function npcraft:agent/init", "    fn('inventory/begin', '''\n        scoreboard players set #iv_ok np.tmp 0\n        scoreboard players set #iv_ready np.tmp 0\n        function npcraft:agent/init\n        execute unless data entity @s data.agent{schema:1} run return 0\n        execute store result score #iv_length np.tmp run data get entity @s data.agent.bag\n        execute unless score #iv_length np.tmp matches 36 run return 0\n        scoreboard players set #iv_ready np.tmp 1")
    for op in ['add_staged','take_staged']:
        s=s.replace("    fn('inventory/"+op+"', '''\n        scoreboard players set #iv_ok np.tmp 0", "    fn('inventory/"+op+"', '''\n        scoreboard players set #iv_ok np.tmp 0\n        execute unless score #iv_ready np.tmp matches 1 run return 0")
# Only standard, breakable unenchanted picks participate in this milestone.
old='f\'execute if data entity @s data.agent.bag[{i}].item{{id:"minecraft:{tool}"}} run scoreboard players set #tool_slot np.tmp {i}\''
new='f\'execute if data entity @s data.agent.bag[{i}].item{{id:"minecraft:{tool}"}} run function npcraft:inventory/pick_candidate {{i:{i},limit:{59 if tool == "wooden_pickaxe" else 131}}}\''
s=s.replace(old,new)
if "fn('inventory/pick_candidate'" not in s:
    addition='''    fn('inventory/pick_candidate', \'''\n        $execute if data entity @s data.agent.bag[$(i)].item.components."minecraft:unbreakable" run return 0
        $execute if data entity @s data.agent.bag[$(i)].item.components."minecraft:enchantments" run return 0
        $execute if data entity @s data.agent.bag[$(i)].item.components."minecraft:max_damage" run return 0
        scoreboard players set #pick_damage np.tmp 0
        $execute store result score #pick_damage np.tmp run data get entity @s data.agent.bag[$(i)].item.components."minecraft:damage"
        $scoreboard players set #pick_limit np.tmp $(limit)
        execute if score #pick_damage np.tmp >= #pick_limit np.tmp run return 0
        execute if score #pick_damage np.tmp matches ..-1 run return 0
        $scoreboard players set #tool_slot np.tmp $(i)
    \''')
'''
    s=s.replace("    fn('inventory/select_slot',",addition+"    fn('inventory/select_slot',")
# Inventory state rather than raw item names decides if a usable pick is present.
needle="        if kind in ('oak_log', 'cobblestone'):"
if "if kind in ('wooden_pickaxe', 'stone_pickaxe'):" not in s:
    extra='''        if kind in ('wooden_pickaxe', 'stone_pickaxe'):
            lines = ['function npcraft:inventory/select_pick']
            if kind == 'wooden_pickaxe':
                lines.append('execute if score #tool_slot np.tmp matches 0..35 run return 1')
            else:
                lines.append('execute if data entity @s data.agent.hand{id:"minecraft:stone_pickaxe"} run return 1')
'''
    s=s.replace(needle,extra+needle)
s=s.replace('''        function npcraft:inventory/count {kind:"stone_pickaxe"}
        execute unless score #iv_have np.tmp matches 1.. run return run function npcraft:planner/need/stone_pickaxe_1''','''        function npcraft:inventory/select_pick
        execute unless data entity @s data.agent.hand{id:"minecraft:stone_pickaxe"} run return run function npcraft:planner/need/stone_pickaxe_1''')
p.write_text(s)
# Geometric edge revalidation also rejects a corrupted non-adjacent first step.
f=p.parents[1]/'datapack/data/npcraft/function/nav/move_macro.mcfunction'
t=f.read_text()
if '#edge_x' not in t:
    lines='''execute store result score #edge_x np.tmp run data get entity @s Pos[0]
execute store result score #edge_z np.tmp run data get entity @s Pos[2]
$data modify storage npcraft:nav x set value $(x)
$data modify storage npcraft:nav z set value $(z)
execute store result score #step_x np.tmp run data get storage npcraft:nav x
execute store result score #step_z np.tmp run data get storage npcraft:nav z
scoreboard players operation #edge_x np.tmp -= #step_x np.tmp
scoreboard players operation #edge_z np.tmp -= #step_z np.tmp
scoreboard players set #negative np.tmp -1
execute if score #edge_x np.tmp matches ..-1 run scoreboard players operation #edge_x np.tmp *= #negative np.tmp
execute if score #edge_z np.tmp matches ..-1 run scoreboard players operation #edge_z np.tmp *= #negative np.tmp
scoreboard players operation #edge_x np.tmp += #edge_z np.tmp
execute unless score #edge_x np.tmp matches 1 run return run function npcraft:nav/blocked
'''
    f.write_text(t.replace('execute store result score #from_y',lines+'execute store result score #from_y'))
f=p.parent/'agent_test.py'
t=f.read_text()
if 'agent_edge_cases' not in t:
    f.write_text(t.replace('    base.TESTS = TESTS','    from tools.agent_edge_cases import TESTS as edge_cases\n    base.TESTS = TESTS + edge_cases'))
