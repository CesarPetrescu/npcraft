execute unless entity @s[type=minecraft:player] run return 0
tag @s remove npcraft.allowed
tellraw @s {"text":"NPCraft access revoked; your companions will pause.","color":"yellow"}
