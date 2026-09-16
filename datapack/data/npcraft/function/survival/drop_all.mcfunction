function npcraft:agent/init
function npcraft:survival/drop_loop {slot:0}
execute if data entity @s data.tool run function npcraft:survival/drop_legacy_tool
execute if data entity @s data.cargo run function npcraft:survival/drop_legacy_cargo
data remove entity @s data.agent.display
