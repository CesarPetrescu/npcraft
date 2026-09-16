execute if data entity @s data.agent{intent:"craft_planks"} run return run function npcraft:actions/planks
execute if data entity @s data.agent{intent:"craft_sticks"} run return run function npcraft:actions/recipes/sticks
execute unless data entity @s data.agent.bench run return run function npcraft:actions/result {state:"blocked",reason:"assign_real_workbench"}
data modify entity @s data.dest set from entity @s data.agent.bench
execute store result score #bench_y np.tmp run data get entity @s data.agent.bench.y
scoreboard players add #bench_y np.tmp 1
execute store result entity @s data.dest.y int 1 run scoreboard players get #bench_y np.tmp
data modify entity @s data.dest.range set value 1
function npcraft:nav/plan
execute if score @s np.status matches 4 run return run function npcraft:actions/result {state:"blocked",reason:"workbench_unreachable"}
execute unless score #arrived np.tmp matches 1 run return run function npcraft:actions/result {state:"running",reason:"moving_to_workbench"}
function npcraft:actions/at_bench with entity @s data.agent.bench
