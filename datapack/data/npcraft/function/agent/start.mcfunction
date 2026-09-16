function npcraft:agent/init
data modify entity @s data.agent.intent set value "idle"
data modify entity @s data.agent.goal set value "stone_pickaxe"
data modify entity @s data.agent.state set value "running"
data modify entity @s data.agent.reason set value "planning"
data modify entity @s data.agent.blocked set value []
data modify entity @s data.agent.failures set value 0
scoreboard players set @s np.mode 4
scoreboard players set @s np.next 0
