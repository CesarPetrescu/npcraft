# Far goals use a strictly improving frontier step. Near unreachable goals stop.
execute store result score #gx np.tmp run data get entity @s data.dest.x
execute store result score #gz np.tmp run data get entity @s data.dest.z
scoreboard players set #minus np.tmp -1
scoreboard players set #best np.tmp 2147483647
execute as @e[tag=npcraft.origin,limit=1] run function npcraft:nav/consider
scoreboard players set #found np.tmp 0
execute as @e[tag=npcraft.node] run function npcraft:nav/consider
