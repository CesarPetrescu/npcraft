$execute unless loaded $(x) $(y) $(z) run return 0
$execute if data entity @s data.agent.blocked[{x:$(x),y:$(y),z:$(z)}] run return 0
$execute if data entity @s data.agent{intent:"gather_logs"} if block $(x) $(y) $(z) minecraft:oak_log run return run function npcraft:work/select_target {x:$(x),y:$(y),z:$(z),kind:"minecraft:oak_log"}
$execute if data entity @s data.agent{intent:"gather_logs"} if block $(x) $(y) $(z) minecraft:birch_log run return run function npcraft:work/select_target {x:$(x),y:$(y),z:$(z),kind:"minecraft:birch_log"}
$execute if data entity @s data.agent{intent:"mine_stone"} if block $(x) $(y) $(z) minecraft:stone run return run function npcraft:work/select_target {x:$(x),y:$(y),z:$(z),kind:"minecraft:stone"}
$execute if data entity @s data.agent{intent:"mine_stone"} if block $(x) $(y) $(z) minecraft:cobblestone run return run function npcraft:work/select_target {x:$(x),y:$(y),z:$(z),kind:"minecraft:cobblestone"}
