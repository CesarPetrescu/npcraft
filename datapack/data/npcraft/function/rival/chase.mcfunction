execute store result score #seen_at np.tmp run data get entity @s data.rival.seen_at
scoreboard players add #seen_at np.tmp 100
execute if score #now np.sys >= #seen_at np.tmp run return run function npcraft:rival/forget
# Track only a stored visible position, never poll the hidden player's current position here.
data modify entity @s data.dest set from entity @s data.rival.last
data modify entity @s data.dest.range set value 2
data remove entity @s data.target
scoreboard players set @s np.dig 0
function npcraft:nav/plan
function npcraft:actions/result {state:"running",reason:"searching_last_seen_position"}
