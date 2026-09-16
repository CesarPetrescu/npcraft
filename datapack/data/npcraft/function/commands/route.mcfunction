scoreboard players operation #selected np.tmp = @s np.sel
scoreboard players set #authorized np.tmp 0
execute as @e[type=minecraft:marker,tag=npcraft.bot,distance=..16] if score @s np.id = #selected np.tmp at @s run function npcraft:commands/authorize with entity @s data
execute unless score #authorized np.tmp matches 1 run tellraw @s {"text":"Select one of your loaded companions within sixteen blocks first.","color":"yellow"}
