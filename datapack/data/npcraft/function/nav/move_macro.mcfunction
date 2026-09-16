# Revalidate the edge, not only its endpoint, after planning.
execute unless function npcraft:nav/cell_safe run return run function npcraft:nav/blocked
$execute positioned $(x) $(y) $(z) unless function npcraft:nav/cell_safe run return run function npcraft:nav/blocked
execute store result score #edge_x np.tmp run data get entity @s Pos[0]
execute store result score #edge_z np.tmp run data get entity @s Pos[2]
$data modify storage npcraft:nav x set value $(x)
$data modify storage npcraft:nav z set value $(z)
execute store result score #step_x np.tmp run data get storage npcraft:nav x
execute store result score #step_z np.tmp run data get storage npcraft:nav z
scoreboard players operation #edge_x np.tmp -= #step_x np.tmp
scoreboard players operation #edge_z np.tmp -= #step_z np.tmp
scoreboard players set #negative np.tmp -1
execute if score #edge_x np.tmp matches ..-1 run scoreboard players operation #edge_x np.tmp *= #negative np.tmp
execute if score #edge_z np.tmp matches ..-1 run scoreboard players operation #edge_z np.tmp *= #negative np.tmp
scoreboard players operation #edge_x np.tmp += #edge_z np.tmp
execute unless score #edge_x np.tmp matches 1 run return run function npcraft:nav/blocked
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
