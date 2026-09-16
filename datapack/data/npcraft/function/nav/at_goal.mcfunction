execute store result score #cell_y np.tmp run data get entity @s Pos[1]
execute unless score #cell_y np.tmp = #goal_y np.tmp run return 0
execute if score #range np.tmp matches 0 if entity @e[tag=npcraft.goal,distance=..0.1] run return 1
execute if score #range np.tmp matches 1 if entity @e[tag=npcraft.goal,distance=..1.1] run return 1
execute if score #range np.tmp matches 2 if entity @e[tag=npcraft.goal,distance=..2.1] run return 1
return 0
