$data modify storage npcraft:inv drop.item set from entity @s data.inventory.slots[$(slot)].item
function npcraft:inventory/drop_item with storage npcraft:inv drop
$execute if score #iv_dropped np.tmp matches 1 run data modify entity @s data.inventory.slots[$(slot)] set value {}
