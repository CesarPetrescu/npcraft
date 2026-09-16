scoreboard players set #pickup_ok np.tmp 0
tag @e[type=minecraft:item,tag=npcraft.pickup] remove npcraft.pickup
$tag @e[type=minecraft:item,tag=npcraft.loot,scores={np.id=$(id)},distance=..1.5,sort=nearest,limit=1] add npcraft.pickup
execute unless entity @e[type=minecraft:item,tag=npcraft.pickup] run return 0
function npcraft:inventory/load
data modify storage npcraft:inv input.item set from entity @e[type=minecraft:item,tag=npcraft.pickup,limit=1] Item
execute store result storage npcraft:inv input.max int 1 run scoreboard players get @e[type=minecraft:item,tag=npcraft.pickup,limit=1] np.count
function npcraft:inventory/insert
execute unless score #inv_ok np.tmp matches 1 run return 0
execute store success score #pickup_ok np.tmp run kill @e[type=minecraft:item,tag=npcraft.pickup,limit=1]
execute if score #pickup_ok np.tmp matches 1 run function npcraft:inventory/commit
