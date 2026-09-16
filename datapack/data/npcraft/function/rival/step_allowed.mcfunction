$data modify storage npcraft:scratch arena_pos set value {x:$(x),y:$(y),z:$(z)}
function npcraft:rival/position_allowed
return run scoreboard players get #arena_ok np.tmp
