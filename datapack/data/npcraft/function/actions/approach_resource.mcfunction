data modify entity @s data.dest set from entity @s data.target
# Bounded plot work starts from its declared floor; full-block height changes remain
# available along the route. Do not target an unsupported mid-air standing cell.
data modify entity @s data.dest.y set from entity @s data.plot.y
data modify entity @s data.dest.range set value 1
function npcraft:nav/plan
