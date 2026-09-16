# Never load a chunk or clear someone's building to force a respawn.
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~ ~0.5 unless function npcraft:nav/cell_safe run return 0
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~ ~0.5 run tp @s ~ ~ ~
data modify entity @s data.survival.dead set value 0b
data modify entity @s data.survival.food set value 10
execute store result score @s np.mode run data get entity @s data.survival.resume_mode
scoreboard players set @s np.next 0
scoreboard players operation #recover_until np.tmp = #now np.sys
scoreboard players add #recover_until np.tmp 400
execute store result entity @s data.survival.recover_until int 1 run scoreboard players get #recover_until np.tmp
data modify entity @s data.survival.recover set from entity @s data.survival.death_pos
execute at @s run function npcraft:bot/sync with entity @s data
function npcraft:survival/body with entity @s data
function npcraft:actions/result {state:"running",reason:"respawned_without_free_items"}
function npcraft:survival/remember_body with entity @s data
