$execute unless loaded $(x) $(y) $(z) run return 0
$execute unless block $(x) $(y) $(z) minecraft:furnace run return 0
# Compare a server-normalized signature saved at placement. Do not take over a replaced furnace.
data remove storage npcraft:scratch station_name
$execute unless data block $(x) $(y) $(z) CustomName run return 0
$data modify storage npcraft:scratch station_name set from block $(x) $(y) $(z) CustomName
execute store success score #pg_different np.tmp run data modify storage npcraft:scratch station_name set from entity @s data.agent.furnace.name
execute unless score #pg_different np.tmp matches 0 run return 0
scoreboard players set #pg_station np.tmp 1
$execute if data block $(x) $(y) $(z) Items[{Slot:0b,id:"minecraft:raw_iron"}] store result score #pg_input np.tmp run data get block $(x) $(y) $(z) Items[{Slot:0b}].count
$execute if data block $(x) $(y) $(z) Items[{Slot:2b,id:"minecraft:iron_ingot"}] store result score #pg_output np.tmp run data get block $(x) $(y) $(z) Items[{Slot:2b}].count
$execute if data block $(x) $(y) $(z) Items[{Slot:1b,id:"minecraft:coal"}] store result score #pg_fuel np.tmp run data get block $(x) $(y) $(z) Items[{Slot:1b}].count
$execute store result score #pg_lit np.tmp run data get block $(x) $(y) $(z) lit_time_remaining
