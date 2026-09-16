# Action boundary: kind allowlist + bounds + reach + visibility + capacity + tool.
execute unless data entity @s data.target{kind:"minecraft:oak_log"} unless data entity @s data.target{kind:"minecraft:birch_log"} unless data entity @s data.target{kind:"minecraft:stone"} unless data entity @s data.target{kind:"minecraft:cobblestone"} run return run function npcraft:actions/invalid_target
execute unless function npcraft:work/in_bounds run return run function npcraft:actions/invalid_target
$execute unless loaded $(x) $(y) $(z) run return run function npcraft:actions/invalid_target
$execute unless block $(x) $(y) $(z) $(kind) run return run function npcraft:actions/invalid_target
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~1 ~0.5 if entity @s[distance=..0.1] run return run function npcraft:actions/result {state:"blocked",reason:"cannot_mine_own_support"}
function npcraft:work/sight with entity @s data.target
execute unless score #visible np.tmp matches 1 run return run function npcraft:actions/result {state:"blocked",reason:"line_of_sight"}
function npcraft:inventory/load
function npcraft:inventory/find_pick
scoreboard players set #mine_stone np.tmp 0
execute if data entity @s data.target{kind:"minecraft:stone"} run scoreboard players set #mine_stone np.tmp 1
execute if data entity @s data.target{kind:"minecraft:cobblestone"} run scoreboard players set #mine_stone np.tmp 1
execute if score #mine_stone np.tmp matches 1 if score #pick_slot np.tmp matches -1 run return run function npcraft:actions/result {state:"blocked",reason:"need_plain_pickaxe"}
$data modify storage npcraft:inv input set value {item:{id:"$(kind)",count:1},max:64}
execute if score #mine_stone np.tmp matches 1 run data modify storage npcraft:inv input.item.id set value "minecraft:cobblestone"
function npcraft:inventory/insert
execute unless score #inv_ok np.tmp matches 1 run return run function npcraft:actions/result {state:"blocked",reason:"backpack_full"}
execute if score #mine_stone np.tmp matches 1 run function npcraft:actions/wear_pick with storage npcraft:inv pick
$execute store success score #ag_broke np.tmp run setblock $(x) $(y) $(z) minecraft:air
execute unless score #ag_broke np.tmp matches 1 run return run function npcraft:actions/invalid_target
function npcraft:inventory/commit
scoreboard players add @s np.harvest 1
function npcraft:work/invalidate
function npcraft:actions/result {state:"succeeded",reason:"resource_collected"}
