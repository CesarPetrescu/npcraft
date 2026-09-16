# Run as the player to approve, e.g. execute as Cesar run function npcraft:admin/grant.
execute unless entity @s[type=minecraft:player] run return 0
tag @s add npcraft.allowed
tellraw @s {"text":"NPCraft access granted. Press G or use /trigger npcraft set 1.","color":"green"}
function npcraft:rival/acl_grant
