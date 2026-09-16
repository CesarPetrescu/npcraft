execute if score #found np.tmp matches 1 run return 1
execute unless entity @e[tag=npcraft.open] run return 0
# Reduce atomically: forked execute conditions are evaluated before their writes.
scoreboard players set #min np.tmp 1000
scoreboard players operation #min np.tmp < @e[tag=npcraft.open] np.depth
execute as @e[tag=npcraft.open] if score @s np.depth = #min np.tmp run tag @s add npcraft.frontier
# Exactly one parent must be visible while inserting its four neighbors.
tag @e[tag=npcraft.frontier,limit=1] add npcraft.current_node
tag @e[tag=npcraft.frontier] remove npcraft.frontier
execute as @e[tag=npcraft.current_node,limit=1] at @s run function npcraft:nav/expand
tag @e[tag=npcraft.current_node] remove npcraft.current_node
execute unless score #found np.tmp matches 1 run function npcraft:nav/search
