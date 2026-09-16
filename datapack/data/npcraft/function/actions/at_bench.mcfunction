$execute unless block $(x) $(y) $(z) minecraft:crafting_table run return run function npcraft:actions/result {state:"blocked",reason:"workbench_missing"}
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~0.5 ~0.5 unless entity @s[distance=..4] run return run function npcraft:actions/result {state:"blocked",reason:"workbench_out_of_reach"}
execute if data entity @s data.agent{intent:"craft_wood_pick"} run return run function npcraft:actions/recipes/wood_pick
execute if data entity @s data.agent{intent:"craft_stone_pick"} run return run function npcraft:actions/recipes/stone_pick
function npcraft:actions/result {state:"blocked",reason:"unsupported_recipe"}
