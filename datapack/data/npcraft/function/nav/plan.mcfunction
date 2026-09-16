function npcraft:nav/cleanup
scoreboard players set #arrived np.tmp 0
scoreboard players set #found np.tmp 0
scoreboard players set #nodes np.tmp 0
execute store result score #range np.tmp run data get entity @s data.dest.range
execute unless function npcraft:nav/cell_safe run return run function npcraft:nav/blocked
function npcraft:nav/goal with entity @s data.dest
execute if function npcraft:nav/at_goal run scoreboard players set #arrived np.tmp 1
execute if score #arrived np.tmp matches 1 run return run function npcraft:nav/arrived
scoreboard players set #cache_moved np.tmp 0
execute if data entity @s data.navigation.steps[0] run function npcraft:nav/cached
execute if score #cache_moved np.tmp matches 1 run return run function npcraft:nav/cleanup
execute summon minecraft:marker run function npcraft:nav/root
function npcraft:nav/search
execute unless score #found np.tmp matches 1 unless entity @e[tag=npcraft.goal,distance=..6] run function npcraft:nav/partial
execute if score #found np.tmp matches 1 run function npcraft:nav/save_route
execute unless score #found np.tmp matches 1 run function npcraft:nav/blocked
function npcraft:nav/cleanup
