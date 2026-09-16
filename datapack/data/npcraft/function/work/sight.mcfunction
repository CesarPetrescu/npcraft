kill @e[type=minecraft:marker,tag=npcraft.ray_target]
$execute positioned $(x) $(y) $(z) positioned ~0.5 ~0.5 ~0.5 run summon minecraft:marker ~ ~ ~ {Tags:["npcraft.ray_target","npcraft.nav"]}
scoreboard players set #visible np.tmp 0
scoreboard players set #ray_budget np.tmp 20
execute positioned ~ ~1.5 ~ if entity @e[tag=npcraft.ray_target,distance=..4.5] facing entity @e[tag=npcraft.ray_target,limit=1] feet store result score #visible np.tmp run function npcraft:work/ray
kill @e[type=minecraft:marker,tag=npcraft.ray_target]
