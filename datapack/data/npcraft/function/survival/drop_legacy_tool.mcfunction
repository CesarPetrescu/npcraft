data modify storage npcraft:scratch death_drop.item set from entity @s data.tool
data modify storage npcraft:scratch death_drop.max set value 1
data modify storage npcraft:scratch death_drop.id set from entity @s data.id
function npcraft:survival/drop_item with storage npcraft:scratch death_drop
execute if score #drop_ok np.tmp matches 1 run data remove entity @s data.tool
