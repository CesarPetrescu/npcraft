# Deliberately conservative: return to the declared home instead of blindly charging.
data modify entity @s data.dest set from entity @s data.home
data modify entity @s data.dest.range set value 0
data remove entity @s data.target
scoreboard players set @s np.dig 0
function npcraft:nav/plan
function npcraft:actions/result {state:"running",reason:"retreating_and_seeking_food"}
