"""One-time feature-branch integration; removed before review."""
from pathlib import Path
p=Path(__file__).resolve().parents[1]
f=p/'datapack/data/npcraft/function'
if 'npcraft:agent/tick' in (f/'bot/brain.mcfunction').read_text():
    raise SystemExit(0)
def wr(path,text): (f/path).write_text(text.strip()+'\n')
a=f/'bot/brain.mcfunction';s=a.read_text().replace('execute at @s run function npcraft:bot/sync','execute if score @s np.mode matches 4 run function npcraft:agent/tick\nexecute at @s run function npcraft:bot/sync');a.write_text(s)
a=f/'bot/sync.mcfunction';a.write_text(a.read_text()+'$execute if score @s np.mode matches 4 if data entity @s data.agent.hand run data modify entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)},limit=1] equipment.mainhand set from entity @s data.agent.hand\n')
a=f/'commands/owned.mcfunction';s=a.read_text().replace('execute if score #cmd np.tmp matches 99','execute if score #cmd np.tmp matches 20..25 run function npcraft:agent/commands\nexecute if score #cmd np.tmp matches 4..11 if data entity @s data.agent run function npcraft:agent/invalidate\nexecute if score #cmd np.tmp matches 99');a.write_text(s)
a=f/'commands/dismiss.mcfunction';a.write_text(a.read_text().replace('function npcraft:commands/drop_cargo','function npcraft:commands/drop_cargo\nfunction npcraft:inventory/drop_all\nexecute if data entity @s data.agent.bag[].item run return 0'))
a=f/'nav/plan.mcfunction';a.write_text(a.read_text().replace('execute unless score #y np.tmp = #goal_y np.tmp run return run function npcraft:nav/blocked\n',''))
wr('nav/expand.mcfunction','''
tag @s remove npcraft.open
execute if function npcraft:nav/at_goal run return run function npcraft:nav/found
scoreboard players operation #depth np.tmp = @s np.depth
scoreboard players set #up_clear np.tmp 0
execute if block ~ ~2 ~ #npcraft:clear run scoreboard players set #up_clear np.tmp 1
execute positioned ~1 ~ ~ run function npcraft:nav/edges
execute positioned ~-1 ~ ~ run function npcraft:nav/edges
execute positioned ~ ~ ~1 run function npcraft:nav/edges
execute positioned ~ ~ ~-1 run function npcraft:nav/edges
''')
wr('nav/edges.mcfunction','''
# Each candidate is one horizontal cell, with at most one block of elevation change.
function npcraft:nav/neighbor
execute if score #up_clear np.tmp matches 1 if block ~ ~ ~ #npcraft:floor positioned ~ ~1 ~ run function npcraft:nav/neighbor
execute if block ~ ~1 ~ #npcraft:clear positioned ~ ~-1 ~ run function npcraft:nav/neighbor
''')
wr('nav/move_macro.mcfunction','''
# Revalidate the edge, not only its endpoint, after planning.
execute unless function npcraft:nav/cell_safe run return run function npcraft:nav/blocked
$execute positioned $(x) $(y) $(z) unless function npcraft:nav/cell_safe run return run function npcraft:nav/blocked
execute store result score #from_y np.tmp run data get entity @s Pos[1]
$data modify storage npcraft:nav y set value $(y)
execute store result score #delta_y np.tmp run data get storage npcraft:nav y
scoreboard players operation #delta_y np.tmp -= #from_y np.tmp
execute unless score #delta_y np.tmp matches -1..1 run return run function npcraft:nav/blocked
execute if score #delta_y np.tmp matches 1 unless block ~ ~2 ~ #npcraft:clear run return run function npcraft:nav/blocked
$execute if score #delta_y np.tmp matches -1 positioned $(x) $(y) $(z) unless block ~ ~2 ~ #npcraft:clear run return run function npcraft:nav/blocked
$tp @s ~ ~ ~ facing $(x) $(y) $(z)
$tp @s $(x) $(y) $(z)
scoreboard players set @s np.status 1
''')
a=f/'nav/consider.mcfunction';s=a.read_text().replace('scoreboard players operation #nx np.tmp += #nz np.tmp','execute store result score #ny np.tmp run data get entity @s Pos[1]\nscoreboard players operation #ny np.tmp -= #goal_y np.tmp\nexecute if score #ny np.tmp matches ..-1 run scoreboard players operation #ny np.tmp *= #minus np.tmp\nscoreboard players operation #nx np.tmp += #ny np.tmp\nscoreboard players operation #nx np.tmp += #nz np.tmp');a.write_text(s)
a=f/'nav/at_goal.mcfunction';a.write_text('execute store result score #cell_y np.tmp run data get entity @s Pos[1]\nexecute unless score #cell_y np.tmp = #goal_y np.tmp run return 0\n'+a.read_text())
for rel in ['project.json','datapack/pack.mcmeta','datapack/data/npcraft/function/load.mcfunction']:
 a=p/rel;a.write_text(a.read_text().replace('0.1.0-alpha.1','0.2.0-alpha.1'))
a=p/'tools/server_test.py';a.write_text(a.read_text().replace('if "0.1.0-alpha.1" in response:','if json.loads((ROOT / "project.json").read_text())["version"] in response:'))
a=p/'tools/validate.py';a.write_text(a.read_text().replace('not relative.endswith("/work/commit.mcfunction")','not any(relative.endswith(allowed) for allowed in ("/work/commit.mcfunction", "/action/commit.mcfunction", "/action/place_table.mcfunction"))'))
