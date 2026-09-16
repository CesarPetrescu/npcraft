execute unless data entity @s data.agent.furnace run return run function npcraft:actions/result {state:"blocked",reason:"furnace_missing"}
data modify entity @s data.dest set from entity @s data.agent.furnace
data modify entity @s data.dest.range set value 1
function npcraft:nav/plan
execute if score @s np.status matches 4 run return run function npcraft:actions/result {state:"blocked",reason:"furnace_unreachable"}
execute unless score #arrived np.tmp matches 1 run return run function npcraft:actions/result {state:"running",reason:"moving_to_furnace"}
function npcraft:stations/operate with entity @s data.agent.furnace
