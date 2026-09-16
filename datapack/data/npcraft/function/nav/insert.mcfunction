tag @s add npcraft.nav
tag @s add npcraft.node
tag @s add npcraft.open
scoreboard players add #nodes np.tmp 1
scoreboard players operation @s np.depth = #depth np.tmp
scoreboard players add @s np.depth 1
data modify entity @s data.first set from entity @e[tag=npcraft.current_node,limit=1] data.first
execute if score #depth np.tmp matches 0 run data modify entity @s data.first set from entity @s Pos
data modify entity @s data.path set from entity @e[tag=npcraft.current_node,limit=1] data.path
data modify entity @s data.path append from entity @s Pos
