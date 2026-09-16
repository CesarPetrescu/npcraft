execute store result score #ag_fail np.tmp run data get entity @s data.agent.failures
scoreboard players add #ag_fail np.tmp 1
execute store result entity @s data.agent.failures int 1 run scoreboard players get #ag_fail np.tmp
execute unless score #ag_fail np.tmp matches 3.. run return 0
data modify entity @s data.agent.blocked append from entity @s data.target
execute store result score #ag_mem np.tmp run data get entity @s data.agent.blocked
execute if score #ag_mem np.tmp matches 9.. run data remove entity @s data.agent.blocked[0]
scoreboard players operation #ag_expiry np.tmp = #now np.sys
scoreboard players add #ag_expiry np.tmp 100
execute store result entity @s data.agent.blocked_until int 1 run scoreboard players get #ag_expiry np.tmp
data modify entity @s data.agent.failures set value 0
function npcraft:work/invalidate
