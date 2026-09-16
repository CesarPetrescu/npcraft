# Inventory is re-read because other goals can have used supplies since the last meal.
function npcraft:inventory/load
$function npcraft:inventory/remove {kind:"$(kind)",count:1}
execute unless score #inv_ok np.tmp matches 1 run return 0
function npcraft:inventory/commit
execute store result score #food np.tmp run data get entity @s data.survival.food
$scoreboard players add #food np.tmp $(food)
execute if score #food np.tmp matches 21.. run scoreboard players set #food np.tmp 20
execute store result entity @s data.survival.food int 1 run scoreboard players get #food np.tmp
scoreboard players operation #eat_at np.tmp = #now np.sys
scoreboard players add #eat_at np.tmp 80
execute store result entity @s data.survival.eat_at int 1 run scoreboard players get #eat_at np.tmp
function npcraft:survival/heal with entity @s data
