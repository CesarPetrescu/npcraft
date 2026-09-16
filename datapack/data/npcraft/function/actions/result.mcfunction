# Shared observable action contract: intent + state + reason, persisted per agent.
$data modify entity @s data.agent.state set value "$(state)"
$data modify entity @s data.agent.reason set value "$(reason)"
