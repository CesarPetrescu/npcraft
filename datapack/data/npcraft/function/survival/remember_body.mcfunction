$execute unless entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)}] run return 0
$data modify storage npcraft:uuid parts set from entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)},limit=1] UUID
function npcraft:identity/encode
data modify entity @s data.survival.body_uuid set from storage npcraft:uuid result
