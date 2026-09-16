execute unless data entity @s data.navigation.steps[0] run return 0
data modify storage npcraft:nav first set from entity @s data.navigation.steps[0]
function npcraft:nav/move
execute if score @s np.status matches 1 run data remove entity @s data.navigation.steps[0]
execute if score @s np.status matches 4 run data remove entity @s data.navigation
