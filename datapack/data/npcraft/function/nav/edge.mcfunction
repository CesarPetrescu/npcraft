# Position is adjacent at source height; executor is the source node.
execute if function npcraft:nav/cell_safe run return run function npcraft:nav/neighbor
execute store result score #up_clear np.tmp run execute at @s if block ~ ~2 ~ #npcraft:clear
execute if score #up_clear np.tmp matches 1 positioned ~ ~1 ~ if function npcraft:nav/cell_safe run function npcraft:nav/neighbor
execute unless block ~ ~ ~ #npcraft:clear run return 0
execute unless block ~ ~1 ~ #npcraft:clear run return 0
execute positioned ~ ~-1 ~ if function npcraft:nav/cell_safe run return run function npcraft:nav/neighbor
execute unless block ~ ~-1 ~ #npcraft:clear run return 0
execute positioned ~ ~-2 ~ if function npcraft:nav/cell_safe run function npcraft:nav/neighbor
