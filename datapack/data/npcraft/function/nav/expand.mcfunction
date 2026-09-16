tag @s remove npcraft.open
execute if function npcraft:nav/at_goal run return run function npcraft:nav/found
scoreboard players operation #depth np.tmp = @s np.depth
scoreboard players set #up_clear np.tmp 0
execute if block ~ ~2 ~ #npcraft:clear run scoreboard players set #up_clear np.tmp 1
execute positioned ~1 ~ ~ run function npcraft:nav/edges
execute positioned ~-1 ~ ~ run function npcraft:nav/edges
execute positioned ~ ~ ~1 run function npcraft:nav/edges
execute positioned ~ ~ ~-1 run function npcraft:nav/edges
