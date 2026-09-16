# Operator diagnostic snapshot; temporary navigation tracing during integration debugging.
data modify storage npcraft:diagnostics snapshot set value {pos:[],dest:{},nodes:0,found:0,arrived:0,range:0,status:0}
data modify storage npcraft:diagnostics snapshot.pos set from entity @s Pos
data modify storage npcraft:diagnostics snapshot.dest set from entity @s data.dest
execute store result storage npcraft:diagnostics snapshot.nodes int 1 run scoreboard players get #nodes np.tmp
execute store result storage npcraft:diagnostics snapshot.found int 1 run scoreboard players get #found np.tmp
execute store result storage npcraft:diagnostics snapshot.arrived int 1 run scoreboard players get #arrived np.tmp
execute store result storage npcraft:diagnostics snapshot.range int 1 run scoreboard players get #range np.tmp
execute store result storage npcraft:diagnostics snapshot.status int 1 run scoreboard players get @s np.status
function npcraft:admin/diagnostic_print with storage npcraft:diagnostics snapshot
