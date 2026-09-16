execute unless function npcraft:work/in_bounds run return run function npcraft:actions/invalid_target
$execute unless block $(x) $(y) $(z) $(kind) run return run function npcraft:actions/invalid_target
# Prefer a currently reachable visible target. An elevated block does not require
# standing at the block's Y; the action boundary still enforces exact ray/reach checks.
function npcraft:work/sight with entity @s data.target
scoreboard players set #arrived np.tmp 0
execute if score #visible np.tmp matches 1 run scoreboard players set #arrived np.tmp 1
execute if score #arrived np.tmp matches 1 run data remove entity @s data.navigation
execute unless score #arrived np.tmp matches 1 run function npcraft:actions/approach_resource
execute if score #arrived np.tmp matches 1 run scoreboard players set @s np.status 0
execute if score @s np.status matches 4 run return run function npcraft:actions/result {state:"blocked",reason:"unreachable"}
execute unless score #arrived np.tmp matches 1 run return run function npcraft:actions/result {state:"running",reason:"moving_to_resource"}
function npcraft:work/sight with entity @s data.target
execute unless score #visible np.tmp matches 1 run return run function npcraft:actions/result {state:"blocked",reason:"line_of_sight"}
function npcraft:actions/result {state:"running",reason:"mining"}
function npcraft:work/swing with entity @s data
execute unless score @s np.dig matches 1.. run function npcraft:actions/start_mine
execute if score #now np.sys < @s np.dig run return 0
function npcraft:actions/mine_commit with entity @s data.target
