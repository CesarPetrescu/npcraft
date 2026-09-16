execute unless function npcraft:rival/access run return 0
execute if data entity @s data.survival{dead:1b} run return 0
function npcraft:survival/recover
execute if score #recovering np.tmp matches 1 run return 0
execute if data entity @s data.rival{retreat:1b} run return run function npcraft:rival/retreat
function npcraft:inventory/load
function npcraft:inventory/find_weapon
execute if score #weapon_damage np.tmp matches 1.. if data entity @s data.rival.last run return run function npcraft:rival/chase
# Independent kit progression continues in loaded chunks without proximity to an opponent.
data modify entity @s data.agent.goal set value "rival_kit"
function npcraft:progression/tick
