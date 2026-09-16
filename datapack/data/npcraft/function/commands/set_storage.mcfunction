execute at @a[tag=npcraft.actor,limit=1] unless block ~ ~-1 ~ minecraft:barrel run return run tellraw @a[tag=npcraft.actor] {"text":"Stand on the barrel you want to assign, then choose Set barrel.","color":"yellow"}
execute store result entity @s data.storage.x int 1 run data get entity @a[tag=npcraft.actor,limit=1] Pos[0]
execute store result score #y np.tmp run data get entity @a[tag=npcraft.actor,limit=1] Pos[1]
scoreboard players remove #y np.tmp 1
execute store result entity @s data.storage.y int 1 run scoreboard players get #y np.tmp
execute store result entity @s data.storage.z int 1 run data get entity @a[tag=npcraft.actor,limit=1] Pos[2]
tellraw @a[tag=npcraft.actor] {"text":"Output barrel assigned. Keep an empty slot and a flat, reachable approach.","color":"green"}
