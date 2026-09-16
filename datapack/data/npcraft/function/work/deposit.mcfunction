execute unless data entity @s data.storage run return run scoreboard players set @s np.status 8
execute unless data entity @s data.cargo run return 0
data modify entity @s data.dest set from entity @s data.storage
execute store result entity @s data.dest.y int 1 run data get entity @s Pos[1]
data modify entity @s data.dest.range set value 1
function npcraft:nav/plan
execute unless score #arrived np.tmp matches 1 run return 0
function npcraft:work/barrel with entity @s data.storage
