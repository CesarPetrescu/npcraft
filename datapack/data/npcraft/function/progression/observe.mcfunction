# Snapshot inventory once, then bounded counters. Station existence is never assumed.
scoreboard players operation #pg_pick np.tmp = #pick_best np.tmp
function npcraft:inventory/count {kind:"minecraft:crafting_table"}
scoreboard players operation #pg_table np.tmp = #iv_total np.tmp
function npcraft:inventory/count {kind:"minecraft:furnace"}
scoreboard players operation #pg_furnace np.tmp = #iv_total np.tmp
function npcraft:inventory/count {kind:"minecraft:coal"}
scoreboard players operation #pg_coal np.tmp = #iv_total np.tmp
function npcraft:inventory/count {kind:"minecraft:raw_iron"}
scoreboard players operation #pg_raw np.tmp = #iv_total np.tmp
function npcraft:inventory/count {kind:"minecraft:iron_ingot"}
scoreboard players operation #pg_iron np.tmp = #iv_total np.tmp
function npcraft:inventory/count {kind:"minecraft:iron_sword"}
scoreboard players operation #pg_sword np.tmp = #iv_total np.tmp
scoreboard players set #pg_bench np.tmp 0
execute if data entity @s data.agent.bench run function npcraft:stations/check_bench with entity @s data.agent.bench
scoreboard players set #pg_station np.tmp 0
scoreboard players set #pg_input np.tmp 0
scoreboard players set #pg_output np.tmp 0
scoreboard players set #pg_fuel np.tmp 0
scoreboard players set #pg_lit np.tmp 0
execute if data entity @s data.agent.furnace run function npcraft:stations/check_furnace with entity @s data.agent.furnace
scoreboard players operation #pg_stock np.tmp = #pg_raw np.tmp
scoreboard players operation #pg_stock np.tmp += #pg_iron np.tmp
scoreboard players operation #pg_stock np.tmp += #pg_input np.tmp
scoreboard players operation #pg_stock np.tmp += #pg_output np.tmp
function npcraft:inventory/find_weapon
scoreboard players set #pg_sword np.tmp 0
execute if score #pick_best np.tmp matches 250 run scoreboard players set #pg_sword np.tmp 1
