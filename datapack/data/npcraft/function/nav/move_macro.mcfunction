# Revalidate the edge, not only its endpoint, after planning.
execute unless function npcraft:nav/cell_safe run return run function npcraft:nav/blocked
$execute positioned $(x) $(y) $(z) unless function npcraft:nav/cell_safe run return run function npcraft:nav/blocked
execute store result score #from_y np.tmp run data get entity @s Pos[1]
$data modify storage npcraft:nav y set value $(y)
execute store result score #delta_y np.tmp run data get storage npcraft:nav y
scoreboard players operation #delta_y np.tmp -= #from_y np.tmp
execute unless score #delta_y np.tmp matches -1..1 run return run function npcraft:nav/blocked
execute if score #delta_y np.tmp matches 1 unless block ~ ~2 ~ #npcraft:clear run return run function npcraft:nav/blocked
$execute if score #delta_y np.tmp matches -1 positioned $(x) $(y) $(z) unless block ~ ~2 ~ #npcraft:clear run return run function npcraft:nav/blocked
$tp @s ~ ~ ~ facing $(x) $(y) $(z)
$tp @s $(x) $(y) $(z)
scoreboard players set @s np.status 1
