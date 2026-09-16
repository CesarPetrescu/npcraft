tag @e[tag=npcraft.owned] remove npcraft.owned
execute as @e[type=minecraft:marker,tag=npcraft.bot,distance=..8] if score @s np.owner = #actor np.tmp run tag @s add npcraft.owned
execute unless entity @e[tag=npcraft.owned] run return run tellraw @s {"text":"No loaded companion of yours within eight blocks.","color":"yellow"}
scoreboard players operation @s np.sel = @e[tag=npcraft.owned,sort=nearest,limit=1] np.id
tag @e[tag=npcraft.owned] remove npcraft.owned
tellraw @s [{"text":"Selected NPCraft #","color":"green"},{"score":{"name":"@s","objective":"np.sel"}}]
