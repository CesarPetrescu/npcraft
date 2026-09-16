execute at @a[tag=npcraft.actor,limit=1] unless block ~ ~-1 ~ minecraft:crafting_table run return run tellraw @a[tag=npcraft.actor] {"text":"Stand on the crafting table to assign it.","color":"yellow"}
execute store result entity @s data.agent.bench.x int 1 run data get entity @a[tag=npcraft.actor,limit=1] Pos[0]
execute store result score #bench_y np.tmp run data get entity @a[tag=npcraft.actor,limit=1] Pos[1]
scoreboard players remove #bench_y np.tmp 1
execute store result entity @s data.agent.bench.y int 1 run scoreboard players get #bench_y np.tmp
execute store result entity @s data.agent.bench.z int 1 run data get entity @a[tag=npcraft.actor,limit=1] Pos[2]
