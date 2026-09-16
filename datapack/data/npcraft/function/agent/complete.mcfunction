function npcraft:actions/result {state:"succeeded",reason:"stone_pickaxe_obtained"}
# Goal remains complete, not a trigger for unbounded resource collection.
function npcraft:inventory/load
function npcraft:inventory/find_pick
execute if score #pick_slot np.tmp matches 0..35 run function npcraft:agent/show_pick with storage npcraft:inv pick
