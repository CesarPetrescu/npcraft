# Transaction workspace; all callers must finish synchronously, without scheduling.
function npcraft:agent/init
data modify storage npcraft:inv slots set from entity @s data.inventory.slots
