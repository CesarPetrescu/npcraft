function npcraft:inventory/count {kind:"logs"}
scoreboard players operation #ag_logs np.tmp = #iv_total np.tmp
execute store result entity @s data.agent.observed.logs int 1 run scoreboard players get #iv_total np.tmp
function npcraft:inventory/count {kind:"planks"}
scoreboard players operation #ag_planks np.tmp = #iv_total np.tmp
execute store result entity @s data.agent.observed.planks int 1 run scoreboard players get #iv_total np.tmp
function npcraft:inventory/count {kind:"minecraft:stick"}
scoreboard players operation #ag_sticks np.tmp = #iv_total np.tmp
execute store result entity @s data.agent.observed.sticks int 1 run scoreboard players get #iv_total np.tmp
function npcraft:inventory/count {kind:"minecraft:cobblestone"}
scoreboard players operation #ag_cobble np.tmp = #iv_total np.tmp
execute store result entity @s data.agent.observed.cobble int 1 run scoreboard players get #iv_total np.tmp
function npcraft:inventory/find_pick
scoreboard players set #ag_wood_pick np.tmp 0
execute if score #pick_slot np.tmp matches 0..35 run scoreboard players set #ag_wood_pick np.tmp 1
execute store result entity @s data.agent.observed.wood_pick int 1 run scoreboard players get #ag_wood_pick np.tmp
scoreboard players set #ag_stone_pick np.tmp 0
execute if score #pick_best np.tmp matches 131.. run scoreboard players set #ag_stone_pick np.tmp 1
execute store result entity @s data.agent.observed.stone_pick int 1 run scoreboard players get #ag_stone_pick np.tmp
execute store result entity @s data.agent.observed.at_tick int 1 run scoreboard players get #now np.sys
