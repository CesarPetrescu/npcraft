tag @e[type=minecraft:item,tag=npcraft.new_drop] remove npcraft.new_drop
$execute store success score #drop_ok np.tmp run summon minecraft:item ~ ~0.5 ~ {Item:$(item),PickupDelay:10s,Tags:["npcraft.loot","npcraft.new_drop"]}
$execute if score #drop_ok np.tmp matches 1 run scoreboard players set @e[type=minecraft:item,tag=npcraft.new_drop,limit=1] np.id $(id)
$execute if score #drop_ok np.tmp matches 1 run scoreboard players set @e[type=minecraft:item,tag=npcraft.new_drop,limit=1] np.count $(max)
tag @e[type=minecraft:item,tag=npcraft.new_drop] remove npcraft.new_drop
