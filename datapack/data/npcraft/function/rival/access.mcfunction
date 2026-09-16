scoreboard players set #rival_access np.tmp 0
function npcraft:rival/access_check with entity @s data
return run scoreboard players get #rival_access np.tmp
