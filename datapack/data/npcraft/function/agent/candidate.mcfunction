$execute unless loaded $(x) $(y) $(z) run return 0
$execute if data entity @s data.agent.blocked[{x:$(x),y:$(y),z:$(z)}] run return 0
$execute if data entity @s data.agent{intent:"gather_logs"} if block $(x) $(y) $(z) minecraft:oak_log run return run function npcraft:work/select_target {x:$(x),y:$(y),z:$(z),kind:"minecraft:oak_log"}
$execute if data entity @s data.agent{intent:"gather_logs"} if block $(x) $(y) $(z) minecraft:birch_log run return run function npcraft:work/select_target {x:$(x),y:$(y),z:$(z),kind:"minecraft:birch_log"}
$execute if data entity @s data.agent{intent:"mine_stone"} if block $(x) $(y) $(z) minecraft:stone run return run function npcraft:work/select_target {x:$(x),y:$(y),z:$(z),kind:"minecraft:stone"}
$execute if data entity @s data.agent{intent:"mine_stone"} if block $(x) $(y) $(z) minecraft:cobblestone run return run function npcraft:work/select_target {x:$(x),y:$(y),z:$(z),kind:"minecraft:cobblestone"}
$execute if data entity @s data.agent{intent:"mine_iron"} if block $(x) $(y) $(z) minecraft:iron_ore run return run function npcraft:work/select_target {x:$(x),y:$(y),z:$(z),kind:"minecraft:iron_ore"}
$execute if data entity @s data.agent{intent:"mine_iron"} if block $(x) $(y) $(z) minecraft:deepslate_iron_ore run return run function npcraft:work/select_target {x:$(x),y:$(y),z:$(z),kind:"minecraft:deepslate_iron_ore"}
$execute if data entity @s data.agent{intent:"mine_coal"} if block $(x) $(y) $(z) minecraft:coal_ore run return run function npcraft:work/select_target {x:$(x),y:$(y),z:$(z),kind:"minecraft:coal_ore"}
$execute if data entity @s data.agent{intent:"mine_coal"} if block $(x) $(y) $(z) minecraft:deepslate_coal_ore run return run function npcraft:work/select_target {x:$(x),y:$(y),z:$(z),kind:"minecraft:deepslate_coal_ore"}
