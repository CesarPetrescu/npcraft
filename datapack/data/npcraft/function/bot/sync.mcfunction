execute if data entity @s data.survival{dead:1b} run return 0
$execute unless entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)}] summon minecraft:mannequin run function npcraft:bot/body_create {id:$(id)}
$tp @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)}] ~ ~ ~ ~ ~
$execute unless score @s np.mode matches 4..6 if data entity @s data.tool run data modify entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)},limit=1] equipment.mainhand set from entity @s data.tool
$execute if data entity @s data.agent.display unless data entity @s data.tool run data modify entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)},limit=1] equipment.mainhand set from entity @s data.agent.display
$execute unless data entity @s data.agent.display unless data entity @s data.tool run item replace entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)}] weapon.mainhand with minecraft:air
$execute if score @s np.mode matches 4..6 if data entity @s data.agent.display run data modify entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)},limit=1] equipment.mainhand set from entity @s data.agent.display
$execute if score @s np.mode matches 4..6 unless data entity @s data.agent.display run item replace entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)}] weapon.mainhand with minecraft:air
execute if data entity @s data.survival{enabled:1b} run function npcraft:survival/body with entity @s data
function npcraft:bot/mark_display with entity @s data
