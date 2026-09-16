function npcraft:actions/result {state:"running",reason:"scanning_assigned_plot"}
execute unless data entity @s data{scanned:196} run return 0
function npcraft:actions/result {state:"blocked",reason:"resources_unavailable"}
scoreboard players operation @s np.next = #now np.sys
scoreboard players add @s np.next 100
data modify entity @s data.scanned set value 0
