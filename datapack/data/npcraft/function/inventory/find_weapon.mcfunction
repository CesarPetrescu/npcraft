# Supported wooden/stone/iron swords use the same descriptive-component policy as tools.
scoreboard players set #pick_slot np.tmp -1
scoreboard players set #pick_best np.tmp 0
function npcraft:inventory/weapon_loop {slot:0}
scoreboard players set #weapon_damage np.tmp 0
execute if score #pick_best np.tmp matches 59 run scoreboard players set #weapon_damage np.tmp 4
execute if score #pick_best np.tmp matches 131 run scoreboard players set #weapon_damage np.tmp 5
execute if score #pick_best np.tmp matches 250 run scoreboard players set #weapon_damage np.tmp 6
