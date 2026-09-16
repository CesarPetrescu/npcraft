execute at @a[tag=npcraft.actor,limit=1] align xyz positioned ~0.5 ~ ~0.5 unless function npcraft:nav/cell_safe run return run tellraw @a[tag=npcraft.actor] {"text":"Stand on supported ground with clear space above.","color":"yellow"}
execute store result entity @s data.plot.x int 1 run data get entity @a[tag=npcraft.actor,limit=1] Pos[0]
execute store result entity @s data.plot.y int 1 run data get entity @a[tag=npcraft.actor,limit=1] Pos[1]
execute store result entity @s data.plot.z int 1 run data get entity @a[tag=npcraft.actor,limit=1] Pos[2]
tellraw @a[tag=npcraft.actor] {"text":"Timber plot set: 7 x 7 blocks, four blocks high. EVERY oak/birch log inside is permitted; do not include buildings.","color":"yellow"}
