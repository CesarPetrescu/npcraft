# One allocated companion per tick. Queue rotation is fair even across unloaded records.
execute unless data storage npcraft:state queue[0] run return 0
data modify storage npcraft:scratch scheduled set from storage npcraft:state queue[0]
data modify storage npcraft:state queue append from storage npcraft:state queue[0]
data remove storage npcraft:state queue[0]
function npcraft:bot/dispatch with storage npcraft:scratch scheduled
