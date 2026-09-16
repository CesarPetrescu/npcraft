function npcraft:agent/init
execute if data entity @s data.survival{enabled:1b} run return 0
function npcraft:bot/sync with entity @s data
execute unless data entity @s data.survival run data modify entity @s data.survival set value {version:1,food:20,dead:0b,deaths:0,enabled:0b}
data modify entity @s data.survival.enabled set value 1b
scoreboard players operation #meal_at np.tmp = #now np.sys
scoreboard players add #meal_at np.tmp 1200
execute store result entity @s data.survival.hunger_at int 1 run scoreboard players get #meal_at np.tmp
data modify entity @s data.survival.health set value 20.0f
function npcraft:survival/body with entity @s data
function npcraft:survival/remember_body with entity @s data
