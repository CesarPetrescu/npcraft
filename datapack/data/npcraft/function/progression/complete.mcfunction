data remove entity @s data.navigation
function npcraft:inventory/load
function npcraft:inventory/find_pick
execute if score #pick_slot np.tmp matches 0..35 run function npcraft:agent/show_pick with storage npcraft:inv pick
function npcraft:actions/result {state:"succeeded",reason:"iron_pickaxe_obtained"}
execute if data entity @s data.agent{goal:"rival_kit"} run function npcraft:actions/result {state:"succeeded",reason:"rival_kit_obtained"}
scoreboard players operation @s np.next = #now np.sys
scoreboard players add @s np.next 40
