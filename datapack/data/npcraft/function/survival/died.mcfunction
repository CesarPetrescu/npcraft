# First mark the tombstone; no presentation sync can resurrect an item-bearing controller.
data modify entity @s data.survival.dead set value 1b
execute store result entity @s data.survival.resume_mode int 1 run scoreboard players get @s np.mode
scoreboard players set @s np.mode 0
data remove entity @s data.navigation
data remove entity @s data.target
scoreboard players set @s np.dig 0
execute store result entity @s data.survival.death_pos.x int 1 run data get entity @s Pos[0]
execute store result entity @s data.survival.death_pos.y int 1 run data get entity @s Pos[1]
execute store result entity @s data.survival.death_pos.z int 1 run data get entity @s Pos[2]
scoreboard players operation #respawn_at np.tmp = #now np.sys
scoreboard players add #respawn_at np.tmp 200
execute store result entity @s data.survival.respawn_at int 1 run scoreboard players get #respawn_at np.tmp
execute store result score #deaths np.tmp run data get entity @s data.survival.deaths
scoreboard players add #deaths np.tmp 1
execute store result entity @s data.survival.deaths int 1 run scoreboard players get #deaths np.tmp
function npcraft:survival/drop_all
function npcraft:actions/result {state:"blocked",reason:"dead_waiting_safe_respawn"}
