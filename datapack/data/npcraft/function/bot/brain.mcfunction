$execute unless entity @a[tag=npcraft.allowed,distance=..64,scores={np.owner=$(owner)},nbt={UUID:$(owner_uuid)}] run return 0
execute if score #now np.sys < @s np.next run return 0
scoreboard players operation @s np.next = #now np.sys
scoreboard players add @s np.next 5
execute if score @s np.mode matches 1 run function npcraft:bot/follow with entity @s data
execute if score @s np.mode matches 2 run function npcraft:bot/home
execute if score @s np.mode matches 3 run function npcraft:work/tick
execute if score @s np.mode matches 4 run function npcraft:agent/tick
execute at @s run function npcraft:bot/sync with entity @s data
