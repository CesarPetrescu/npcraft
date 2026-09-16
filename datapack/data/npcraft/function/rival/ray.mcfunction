execute if entity @e[type=minecraft:marker,tag=npcraft.vision,distance=..0.3] run return 1
execute unless block ~ ~ ~ #npcraft:clear run return 0
execute unless score #vision_budget np.tmp matches 1.. run return 0
scoreboard players remove #vision_budget np.tmp 1
return run execute positioned ^ ^ ^0.25 run function npcraft:rival/ray
