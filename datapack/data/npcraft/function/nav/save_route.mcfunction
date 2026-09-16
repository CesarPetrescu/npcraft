data modify entity @s data.navigation.goal set from entity @s data.dest
data modify entity @s data.navigation.steps set from storage npcraft:nav route
function npcraft:nav/advance
