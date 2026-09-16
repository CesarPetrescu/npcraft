# Internal recipe called only by the validated craft action.
function npcraft:inventory/load
function npcraft:inventory/remove {kind:"minecraft:birch_log",count:1}
execute unless score #inv_ok np.tmp matches 1 run return run function npcraft:actions/result {state:"blocked",reason:"missing_ingredients"}
data modify storage npcraft:inv input set value {item:{id:"minecraft:birch_planks",count:4},max:64}
function npcraft:inventory/insert
execute unless score #inv_ok np.tmp matches 1 run return run function npcraft:actions/result {state:"blocked",reason:"backpack_full"}
function npcraft:inventory/commit
function npcraft:actions/result {state:"succeeded",reason:"crafted"}
