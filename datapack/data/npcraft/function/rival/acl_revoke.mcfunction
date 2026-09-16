execute store result storage npcraft:scratch acl.id int 1 run scoreboard players get @s np.owner
data modify storage npcraft:scratch acl.allowed set value 0b
function npcraft:rival/acl_write with storage npcraft:scratch acl
