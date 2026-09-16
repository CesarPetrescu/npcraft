function npcraft:agent/init
execute unless data entity @s data.plot run return run function npcraft:actions/result {state:"blocked",reason:"assign_work_plot"}
execute store result score #ag_expiry np.tmp run data get entity @s data.agent.blocked_until
execute if score #now np.sys >= #ag_expiry np.tmp run data modify entity @s data.agent.blocked set value []
function npcraft:inventory/load
function npcraft:agent/observe
function npcraft:progression/observe
function npcraft:progression/plan
function npcraft:progression/run
