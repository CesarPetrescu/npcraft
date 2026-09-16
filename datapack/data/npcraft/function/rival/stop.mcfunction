data modify entity @s data.rival.enabled set value 0b
data remove entity @s data.rival.last
data remove entity @s data.navigation
scoreboard players set @s np.mode 0
function npcraft:actions/result {state:"cancelled",reason:"rival_stopped"}
