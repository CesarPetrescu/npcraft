data modify storage npcraft:scratch death_drop.item set from entity @s data.cargo
data modify storage npcraft:scratch death_drop.max set value 64
data modify storage npcraft:scratch death_drop.id set from entity @s data.id
function npcraft:survival/drop_item with storage npcraft:scratch death_drop
execute if score #drop_ok np.tmp matches 1 run data remove entity @s data.cargo
