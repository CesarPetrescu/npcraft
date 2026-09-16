# Internal recipe called only by the validated craft action.
function npcraft:inventory/load
function npcraft:inventory/remove {kind:"planks",count:3}
execute unless score #inv_ok np.tmp matches 1 run return run function npcraft:actions/result {state:"blocked",reason:"missing_ingredients"}
function npcraft:inventory/remove {kind:"minecraft:stick",count:2}
execute unless score #inv_ok np.tmp matches 1 run return run function npcraft:actions/result {state:"blocked",reason:"missing_ingredients"}
data modify storage npcraft:inv input set value {item:{id:"minecraft:wooden_pickaxe",count:1,components:{"minecraft:damage":0}},max:1}
function npcraft:inventory/insert
execute unless score #inv_ok np.tmp matches 1 run return run function npcraft:actions/result {state:"blocked",reason:"backpack_full"}
function npcraft:inventory/commit
function npcraft:actions/result {state:"succeeded",reason:"crafted"}
data modify entity @s data.agent.display set from storage npcraft:inv input.item
