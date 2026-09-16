execute if score @s np.count matches 4.. run return run tellraw @s {"text":"Limit reached: four allocated companions per owner (including unloaded ones).","color":"yellow"}
execute if score #total np.sys matches 16.. run return run tellraw @s {"text":"Server allocation limit reached: sixteen companions.","color":"yellow"}
execute align xyz positioned ~0.5 ~ ~0.5 unless function npcraft:nav/cell_safe run return run tellraw @s {"text":"Stand on supported full-block ground with clear space above you.","color":"yellow"}
scoreboard players add #next np.sys 1
execute align xyz positioned ~0.5 ~ ~0.5 summon minecraft:marker run function npcraft:bot/create
scoreboard players add @s np.count 1
scoreboard players add #total np.sys 1
scoreboard players operation @s np.sel = #next np.sys
tellraw @s {"text":"Companion recruited and selected. Press G to give an order.","color":"green"}
