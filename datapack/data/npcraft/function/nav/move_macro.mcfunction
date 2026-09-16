$execute positioned $(x) $(y) $(z) unless function npcraft:nav/cell_safe run return run function npcraft:nav/blocked
$tp @s ~ ~ ~ facing $(x) $(y) $(z)
$tp @s $(x) $(y) $(z)
scoreboard players set @s np.status 1
