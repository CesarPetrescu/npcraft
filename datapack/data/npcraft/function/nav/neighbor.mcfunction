execute if score #nodes np.tmp matches 128.. run return 0
execute if entity @e[tag=npcraft.node,distance=..0.1] run return 0
execute unless entity @e[tag=npcraft.origin,distance=..6] run return 0
execute unless function npcraft:nav/cell_safe run return 0
execute summon minecraft:marker run function npcraft:nav/insert
