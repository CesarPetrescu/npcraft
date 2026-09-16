execute if score #found np.tmp matches 1 run return 1
execute unless entity @e[tag=npcraft.open] run return 0
# Nodes are bounded during insertion; closed nodes are never reopened.
scoreboard players set #min np.tmp 1000
execute as @e[tag=npcraft.open] if score @s np.depth < #min np.tmp run scoreboard players operation #min np.tmp = @s np.depth
execute as @e[tag=npcraft.open] if score @s np.depth = #min np.tmp unless entity @e[tag=npcraft.current_node] run tag @s add npcraft.current_node
execute as @e[tag=npcraft.current_node,limit=1] at @s run function npcraft:nav/expand
tag @e[tag=npcraft.current_node] remove npcraft.current_node
execute unless score #found np.tmp matches 1 run function npcraft:nav/search
