execute unless data entity @s data.rival{enabled:1b} run return 0
execute unless function npcraft:rival/access run return 0
execute store result score #react_at np.tmp run data get entity @s data.rival.react_at
execute if score #now np.sys < #react_at np.tmp run return 0
scoreboard players operation #react_at np.tmp = #now np.sys
scoreboard players add #react_at np.tmp 5
execute store result entity @s data.rival.react_at int 1 run scoreboard players get #react_at np.tmp
function npcraft:rival/perceive with entity @s data.rival
execute store result score #hp np.tmp run data get entity @s data.survival.health
execute if score #hp np.tmp matches ..6 run function npcraft:rival/enter_retreat
execute if score #hp np.tmp matches 14.. run data modify entity @s data.rival.retreat set value 0b
execute if data entity @s data.rival{retreat:1b} run return 0
execute if score #seen np.tmp matches 1 run function npcraft:rival/attack with entity @s data
