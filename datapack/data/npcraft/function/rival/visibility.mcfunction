kill @e[type=minecraft:marker,tag=npcraft.vision]
execute at @a[tag=npcraft.opponent,limit=1] positioned ~ ~1.5 ~ run summon minecraft:marker ~ ~ ~ {Tags:["npcraft.vision"]}
scoreboard players set #vision_budget np.tmp 66
execute positioned ~ ~1.5 ~ facing entity @e[type=minecraft:marker,tag=npcraft.vision,limit=1] feet store result score #seen np.tmp run function npcraft:rival/ray
kill @e[type=minecraft:marker,tag=npcraft.vision]
