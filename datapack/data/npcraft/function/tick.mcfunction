execute unless data storage npcraft:meta {schema:1} run return 0
execute as @a unless score @s np.owner matches 1.. run function npcraft:player/init
scoreboard players enable @a npcraft
execute as @a[scores={npcraft=1..}] at @s run function npcraft:commands/dispatch
execute as @a[scores={npcraft=..-1}] run scoreboard players set @s npcraft 0
execute if score #enabled np.sys matches 1 store result score #now np.sys run time query gametime
execute in minecraft:overworld run function npcraft:runtime/tick
execute unless score #enabled np.sys matches 1 run return 0
execute in minecraft:overworld run function npcraft:scheduler
