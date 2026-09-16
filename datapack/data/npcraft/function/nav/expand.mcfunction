tag @s remove npcraft.open
execute if function npcraft:nav/at_goal run return run function npcraft:nav/found
scoreboard players operation #depth np.tmp = @s np.depth
execute positioned ~1 ~ ~ run function npcraft:nav/neighbor
execute positioned ~-1 ~ ~ run function npcraft:nav/neighbor
execute positioned ~ ~ ~1 run function npcraft:nav/neighbor
execute positioned ~ ~ ~-1 run function npcraft:nav/neighbor
