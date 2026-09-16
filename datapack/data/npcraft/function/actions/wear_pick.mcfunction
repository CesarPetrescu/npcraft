scoreboard players set #pick_damage np.tmp 0
$execute store result score #pick_damage np.tmp run data get storage npcraft:inv slots[$(slot)].item.components."minecraft:damage"
scoreboard players add #pick_damage np.tmp 1
$execute store result storage npcraft:inv slots[$(slot)].item.components."minecraft:damage" int 1 run scoreboard players get #pick_damage np.tmp
$data modify entity @s data.agent.display set from storage npcraft:inv slots[$(slot)].item
$execute if score #pick_damage np.tmp matches $(durability).. run data modify storage npcraft:inv slots[$(slot)] set value {}
$execute if score #pick_damage np.tmp matches $(durability).. run data remove entity @s data.agent.display
