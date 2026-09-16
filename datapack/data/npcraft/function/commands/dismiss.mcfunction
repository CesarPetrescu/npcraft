function npcraft:commands/drop_tool
function npcraft:commands/drop_cargo
execute if data entity @s data.tool run return 0
execute if data entity @s data.cargo run return 0
# Clear the visual copy BEFORE kill so dismissal cannot duplicate the real axe.
$item replace entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)}] weapon.mainhand with minecraft:air
$kill @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)}]
$data remove storage npcraft:state queue[{id:$(id)}]
scoreboard players remove #total np.sys 1
scoreboard players remove @a[tag=npcraft.actor,limit=1] np.count 1
scoreboard players set @a[tag=npcraft.actor,limit=1] np.sel 0
kill @s
