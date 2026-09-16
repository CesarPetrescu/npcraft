# Revalidate both destination and emptiness in the same synchronous command chain.
$execute unless block $(x) $(y) $(z) minecraft:barrel run return 0
$execute if items block $(x) $(y) $(z) container.$(slot) * run return 0
$execute store success score #transferred np.tmp run item replace block $(x) $(y) $(z) container.$(slot) with $(kind) $(count)
execute if score #transferred np.tmp matches 1 run data remove entity @s data.cargo
execute if score #transferred np.tmp matches 1 run data modify entity @s data.scanned set value 0
