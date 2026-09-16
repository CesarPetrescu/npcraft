# A declared simplified food meter, not a claim of vanilla player saturation/exhaustion.
execute if score #food np.tmp matches 1.. run scoreboard players remove #food np.tmp 1
execute store result entity @s data.survival.food int 1 run scoreboard players get #food np.tmp
scoreboard players operation #hunger_at np.tmp = #now np.sys
scoreboard players add #hunger_at np.tmp 1200
execute store result entity @s data.survival.hunger_at int 1 run scoreboard players get #hunger_at np.tmp
