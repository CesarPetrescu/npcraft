# First step must remain adjacent and pass its full swept block-column checks.
$execute store result score #step_safe np.tmp run function npcraft:nav/step_safe {x:$(x),y:$(y),z:$(z)}
execute unless score #step_safe np.tmp matches 1 run return run function npcraft:nav/blocked
$tp @s ~ ~ ~ facing $(x) $(y) $(z)
$tp @s $(x) $(y) $(z)
scoreboard players set @s np.status 1
scoreboard players operation #move_at np.tmp = #now np.sys
scoreboard players add #move_at np.tmp 5
execute store result entity @s data.move_at int 1 run scoreboard players get #move_at np.tmp
