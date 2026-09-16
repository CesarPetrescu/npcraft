execute unless data entity @s data.target run function npcraft:agent/scan
execute unless data entity @s data.target run return run function npcraft:agent/no_target
function npcraft:actions/mine with entity @s data.target
execute if data entity @s data.agent{state:"blocked",reason:"unreachable"} run function npcraft:agent/failure
execute if data entity @s data.agent{state:"blocked",reason:"line_of_sight"} run function npcraft:agent/failure
