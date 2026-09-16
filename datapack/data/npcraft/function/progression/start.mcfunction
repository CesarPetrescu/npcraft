function npcraft:agent/init
data modify entity @s data.agent.goal set value "iron_pickaxe"
data modify entity @s data.agent.intent set value "idle"
data modify entity @s data.agent.blocked set value []
data remove entity @s data.target
scoreboard players set @s np.dig 0
scoreboard players set @s np.mode 5
scoreboard players set @s np.next 0
function npcraft:actions/result {state:"running",reason:"planning_iron"}
