function npcraft:inventory/load
function npcraft:inventory/count {kind:"minecraft:raw_iron"}
execute unless score #iv_total np.tmp matches 1.. run return 0
# Feed one item per visit: native cooking owns the in-flight item, never a phantom counter.
function npcraft:inventory/remove {kind:"minecraft:raw_iron",count:1}
execute unless score #inv_ok np.tmp matches 1 run return 0
$execute if items block $(x) $(y) $(z) container.0 * run return 0
$execute store success score #fed np.tmp run item replace block $(x) $(y) $(z) container.0 with minecraft:raw_iron 1
execute if score #fed np.tmp matches 1 run function npcraft:inventory/commit
