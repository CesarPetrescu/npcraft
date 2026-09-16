$execute unless loaded $(x) $(y) $(z) run return 0
$execute if block $(x) $(y) $(z) minecraft:oak_log run return run function npcraft:work/select_target {x:$(x),y:$(y),z:$(z),kind:"minecraft:oak_log"}
$execute if block $(x) $(y) $(z) minecraft:birch_log run return run function npcraft:work/select_target {x:$(x),y:$(y),z:$(z),kind:"minecraft:birch_log"}
