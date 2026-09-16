tag @s add npcraft.nav
tag @s add npcraft.node
tag @s add npcraft.open
tag @s add npcraft.origin
scoreboard players set @s np.depth 0
scoreboard players set #nodes np.tmp 1
data modify entity @s data.first set from entity @s Pos
data modify entity @s data.path set value []
