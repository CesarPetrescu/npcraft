execute if data entity @s data.agent{intent:"iron_complete"} run return run function npcraft:progression/complete
execute if data entity @s data.agent{intent:"kit_complete"} run return run function npcraft:progression/complete
execute if data entity @s data.agent{intent:"mine_iron"} run return run function npcraft:agent/gather
execute if data entity @s data.agent{intent:"mine_coal"} run return run function npcraft:agent/gather
execute if data entity @s data.agent{intent:"craft_table"} run return run function npcraft:actions/recipes/table
execute if data entity @s data.agent{intent:"place_table"} run return run function npcraft:stations/place {kind:"minecraft:crafting_table",key:"bench"}
execute if data entity @s data.agent{intent:"place_furnace"} run return run function npcraft:stations/place {kind:"minecraft:furnace",key:"furnace"}
execute if data entity @s data.agent{intent:"craft_furnace"} run return run function npcraft:actions/craft
execute if data entity @s data.agent{intent:"craft_iron_pick"} run return run function npcraft:actions/craft
execute if data entity @s data.agent{intent:"craft_iron_sword"} run return run function npcraft:actions/craft
execute if data entity @s data.agent{intent:"smelt"} run return run function npcraft:stations/smelt
function npcraft:actions/run
