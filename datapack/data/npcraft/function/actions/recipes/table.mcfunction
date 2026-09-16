# All-or-nothing logical recipe transaction; no server tick can interleave.
function npcraft:inventory/load
function npcraft:inventory/remove {kind:"planks",count:4}
execute unless score #inv_ok np.tmp matches 1 run return run function npcraft:actions/result {state:"blocked",reason:"missing_ingredients"}
data modify storage npcraft:inv input set value {"item":{"id":"minecraft:crafting_table","count":1},"max":64}
function npcraft:inventory/insert
execute unless score #inv_ok np.tmp matches 1 run return run function npcraft:actions/result {state:"blocked",reason:"backpack_full"}
function npcraft:inventory/commit
function npcraft:actions/result {state:"succeeded",reason:"crafted"}
