$execute unless entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)}] summon minecraft:mannequin run function npcraft:bot/body_create {id:$(id)}
$tp @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)}] ~ ~ ~ ~ ~
$execute if data entity @s data.tool run data modify entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)},limit=1] equipment.mainhand set from entity @s data.tool
$execute unless data entity @s data.tool run item replace entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)}] weapon.mainhand with minecraft:air
