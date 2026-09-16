# Cap equals the allocation cap. Every chain finishes synchronously; no shared scratch survives.
execute as @e[type=minecraft:marker,tag=npcraft.bot,limit=16] at @s run function npcraft:runtime/fast with entity @s data
# Native drop copies carry a reserved component; authoritative returned items never do.
kill @e[type=minecraft:item,nbt={Item:{components:{"minecraft:custom_data":{npcraft_visual:1b}}}}]
