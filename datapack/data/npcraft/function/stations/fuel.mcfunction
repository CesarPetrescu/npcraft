function npcraft:inventory/load
function npcraft:inventory/remove {kind:"minecraft:coal",count:1}
execute unless score #inv_ok np.tmp matches 1 run return 0
$execute if items block $(x) $(y) $(z) container.1 * run return 0
$execute store success score #fed np.tmp run item replace block $(x) $(y) $(z) container.1 with minecraft:coal 1
execute if score #fed np.tmp matches 1 run function npcraft:inventory/commit
