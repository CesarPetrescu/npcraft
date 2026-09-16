execute if data entity @s data.survival{dead:1b} run return 0
$execute unless data entity @s data.rival{enabled:1b} unless entity @a[tag=npcraft.allowed,distance=..64,scores={np.owner=$(owner)},nbt={UUID:$(owner_uuid)}] run return 0
execute if data entity @s data.rival{enabled:1b} unless function npcraft:rival/access run return 0
execute if score #now np.sys < @s np.next run return 0
scoreboard players operation @s np.next = #now np.sys
scoreboard players add @s np.next 5
execute if score @s np.mode matches 1 run function npcraft:bot/follow with entity @s data
execute if score @s np.mode matches 2 run function npcraft:bot/home
execute if score @s np.mode matches 3 run function npcraft:work/tick
execute if score @s np.mode matches 4 run function npcraft:agent/tick
execute if score @s np.mode matches 5 run function npcraft:survival/recover
execute if score @s np.mode matches 5 unless score #recovering np.tmp matches 1 run function npcraft:progression/tick
execute if score @s np.mode matches 6 run function npcraft:rival/think
execute at @s run function npcraft:bot/sync with entity @s data
