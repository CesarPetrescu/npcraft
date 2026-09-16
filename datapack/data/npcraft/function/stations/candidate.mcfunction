execute unless loaded ~ ~ ~ run return 0
execute unless block ~ ~ ~ minecraft:air run return 0
execute align xyz if entity @e[type=!minecraft:marker,dx=0,dy=0,dz=0] run return 0
execute unless function npcraft:nav/cell_safe run return 0
execute if entity @e[type=minecraft:marker,tag=npcraft.bot,distance=..0.7] run return 0
# Obtain coordinates from a short-lived marker, never from a player-controlled string.
execute summon minecraft:marker run function npcraft:stations/position
$data modify storage npcraft:scratch station.kind set value "$(kind)"
$data modify storage npcraft:scratch station.key set value "$(key)"
data modify storage npcraft:scratch station.id set from entity @s data.id
execute at @s run function npcraft:stations/place_commit with storage npcraft:scratch station
