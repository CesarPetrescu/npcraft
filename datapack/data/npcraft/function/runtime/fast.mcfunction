execute if data entity @s data.survival{enabled:1b} run function npcraft:survival/tick with entity @s data
execute if data entity @s data.survival{dead:1b} run return 0
execute unless score #enabled np.sys matches 1 run return 0
$execute unless data entity @s data.rival{enabled:1b} unless entity @a[tag=npcraft.allowed,distance=..64,scores={np.owner=$(owner)},nbt={UUID:$(owner_uuid)}] run return 0
execute if data entity @s data.rival{enabled:1b} unless function npcraft:rival/access run return 0
execute unless score @s np.mode matches 1..6 run return 0
# Rival perception/attack stays responsive even while another worker owns the planner budget.
execute if score @s np.mode matches 6 run function npcraft:rival/react with entity @s data
scoreboard players set #move_at np.tmp 0
execute store result score #move_at np.tmp run data get entity @s data.move_at
execute if score #now np.sys < #move_at np.tmp run return 0
execute if data entity @s data.navigation.steps[0] run function npcraft:nav/advance
execute at @s run function npcraft:bot/sync with entity @s data
