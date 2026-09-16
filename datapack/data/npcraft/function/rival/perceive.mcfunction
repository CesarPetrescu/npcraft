# This selector identifies an opted-in opponent; coordinates are read ONLY after LOS succeeds.
scoreboard players set #seen np.tmp 0
tag @a[tag=npcraft.opponent] remove npcraft.opponent
$tag @a[nbt={UUID:$(opponent)},gamemode=!creative,gamemode=!spectator,distance=..16,limit=1] add npcraft.opponent
execute unless entity @a[tag=npcraft.opponent] run return 0
execute store result score #enemy_health np.tmp run data get entity @a[tag=npcraft.opponent,limit=1] Health
execute unless score #enemy_health np.tmp matches 1.. run return run function npcraft:rival/finish
# Check declared arena before any sensing/attack, but do not store these scratch coordinates in memory.
execute store result storage npcraft:scratch arena_pos.x int 1 run data get entity @a[tag=npcraft.opponent,limit=1] Pos[0]
execute store result storage npcraft:scratch arena_pos.y int 1 run data get entity @a[tag=npcraft.opponent,limit=1] Pos[1]
execute store result storage npcraft:scratch arena_pos.z int 1 run data get entity @a[tag=npcraft.opponent,limit=1] Pos[2]
function npcraft:rival/position_allowed
execute unless score #arena_ok np.tmp matches 1 run return 0
function npcraft:rival/visibility
execute unless score #seen np.tmp matches 1 run return 0
data modify entity @s data.rival.last set from storage npcraft:scratch arena_pos
execute store result entity @s data.rival.seen_at int 1 run scoreboard players get #now np.sys
