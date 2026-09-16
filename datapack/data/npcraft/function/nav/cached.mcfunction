data modify storage npcraft:nav compare set from entity @s data.navigation.goal
execute store success score #cache_changed np.tmp run data modify storage npcraft:nav compare set from entity @s data.dest
execute if score #cache_changed np.tmp matches 1 run return 0
function npcraft:nav/advance
execute if score @s np.status matches 1 run scoreboard players set #cache_moved np.tmp 1
