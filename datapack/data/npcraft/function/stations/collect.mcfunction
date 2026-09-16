function npcraft:inventory/load
$data modify storage npcraft:inv input.item set from block $(x) $(y) $(z) Items[{Slot:2b}]
data remove storage npcraft:inv input.item.Slot
data modify storage npcraft:inv input.max set value 64
function npcraft:inventory/insert
execute unless score #inv_ok np.tmp matches 1 run return run function npcraft:actions/result {state:"blocked",reason:"backpack_full"}
$execute store success score #taken np.tmp run item replace block $(x) $(y) $(z) container.2 with minecraft:air
execute unless score #taken np.tmp matches 1 run return 0
function npcraft:inventory/commit
function npcraft:actions/result {state:"succeeded",reason:"native_furnace_output_collected"}
