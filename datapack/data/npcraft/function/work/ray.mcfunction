# A hit succeeds only inside the exact target block, not merely near it.
execute align xyz positioned ~0.5 ~0.5 ~0.5 if entity @e[tag=npcraft.ray_target,distance=..0.1] run return 1
execute unless block ~ ~ ~ #npcraft:clear run return 0
execute unless score #ray_budget np.tmp matches 1.. run return 0
scoreboard players remove #ray_budget np.tmp 1
return run execute positioned ^ ^ ^0.25 run function npcraft:work/ray
