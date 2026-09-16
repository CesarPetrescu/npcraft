$data modify storage npcraft:ui row set from entity @s data.inventory.slots[$(slot)].item
$data modify storage npcraft:ui row.slot set value $(slot)
function npcraft:ui/row_append with storage npcraft:ui row
