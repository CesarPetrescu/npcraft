$data modify storage npcraft:scratch death_drop set from entity @s data.inventory.slots[$(slot)]
data modify storage npcraft:scratch death_drop.id set from entity @s data.id
function npcraft:survival/drop_item with storage npcraft:scratch death_drop
$execute if score #drop_ok np.tmp matches 1 run data modify entity @s data.inventory.slots[$(slot)] set value {}
