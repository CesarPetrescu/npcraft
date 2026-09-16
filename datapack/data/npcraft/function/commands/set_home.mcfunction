execute at @a[tag=npcraft.actor,limit=1] align xyz positioned ~0.5 ~ ~0.5 unless function npcraft:nav/cell_safe run return run tellraw @a[tag=npcraft.actor] {"text":"Stand on supported ground with clear space above.","color":"yellow"}
execute store result entity @s data.home.x int 1 run data get entity @a[tag=npcraft.actor,limit=1] Pos[0]
execute store result entity @s data.home.y int 1 run data get entity @a[tag=npcraft.actor,limit=1] Pos[1]
execute store result entity @s data.home.z int 1 run data get entity @a[tag=npcraft.actor,limit=1] Pos[2]
tellraw @a[tag=npcraft.actor] {"text":"Home set at your feet.","color":"yellow"}
