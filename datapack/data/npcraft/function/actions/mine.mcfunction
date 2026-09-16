execute unless function npcraft:work/in_bounds run return run function npcraft:actions/invalid_target
$execute unless block $(x) $(y) $(z) $(kind) run return run function npcraft:actions/invalid_target
data modify entity @s data.dest set from entity @s data.target
execute if data entity @s data.agent{intent:"gather_logs"} run data modify entity @s data.dest.y set from entity @s data.plot.y
data modify entity @s data.dest.range set value 1
function npcraft:nav/plan
execute if score @s np.status matches 4 run return run function npcraft:actions/result {state:"blocked",reason:"unreachable"}
execute unless score #arrived np.tmp matches 1 run return run function npcraft:actions/result {state:"running",reason:"moving_to_resource"}
function npcraft:work/sight with entity @s data.target
execute unless score #visible np.tmp matches 1 run return run function npcraft:actions/result {state:"blocked",reason:"line_of_sight"}
function npcraft:actions/result {state:"running",reason:"mining"}
function npcraft:work/swing with entity @s data
execute unless score @s np.dig matches 1.. run function npcraft:actions/start_mine
execute if score #now np.sys < @s np.dig run return 0
function npcraft:actions/mine_commit with entity @s data.target
