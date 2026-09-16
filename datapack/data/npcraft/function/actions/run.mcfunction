# No caller-controlled function names or commands. Every action validates its own world effects.
execute if data entity @s data.agent{intent:"complete"} run return run function npcraft:agent/complete
execute if data entity @s data.agent{intent:"gather_logs"} run return run function npcraft:agent/gather
execute if data entity @s data.agent{intent:"mine_stone"} run return run function npcraft:agent/gather
execute if data entity @s data.agent{intent:"craft_planks"} run return run function npcraft:actions/craft
execute if data entity @s data.agent{intent:"craft_sticks"} run return run function npcraft:actions/craft
execute if data entity @s data.agent{intent:"craft_wood_pick"} run return run function npcraft:actions/craft
execute if data entity @s data.agent{intent:"craft_stone_pick"} run return run function npcraft:actions/craft
function npcraft:actions/result {state:"blocked",reason:"unsupported_action"}
