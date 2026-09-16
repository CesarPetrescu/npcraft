scoreboard players set #pg_station np.tmp 0
function npcraft:stations/check_furnace with entity @s data.agent.furnace
execute unless score #pg_station np.tmp matches 1 run return run function npcraft:actions/result {state:"blocked",reason:"furnace_missing_or_replaced"}
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~0.5 ~0.5 unless entity @s[distance=..3] run return run function npcraft:actions/result {state:"blocked",reason:"furnace_out_of_reach"}
function npcraft:work/sight with entity @s data.agent.furnace
execute unless score #visible np.tmp matches 1 run return run function npcraft:actions/result {state:"blocked",reason:"furnace_line_of_sight"}
$execute if items block $(x) $(y) $(z) container.2 minecraft:iron_ingot run return run function npcraft:stations/collect with entity @s data.agent.furnace
$execute if items block $(x) $(y) $(z) container.2 * run return run function npcraft:actions/result {state:"blocked",reason:"foreign_furnace_output"}
$execute unless items block $(x) $(y) $(z) container.0 * run function npcraft:stations/feed with entity @s data.agent.furnace
$execute unless items block $(x) $(y) $(z) container.1 * if score #pg_lit np.tmp matches 0 run function npcraft:stations/fuel with entity @s data.agent.furnace
function npcraft:actions/result {state:"running",reason:"waiting_for_real_smelting"}
