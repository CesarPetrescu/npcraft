# Attack has its own live consent/arena/LOS/reach/cooldown checks, not just the planner's belief.
execute unless data entity @s data.rival{enabled:1b,retreat:0b} run return 0
execute unless function npcraft:rival/access run return 0
execute unless score @s np.mode matches 6 run return 0
execute if data entity @s data.survival{dead:1b} run return 0
function npcraft:rival/perceive with entity @s data.rival
execute unless score #seen np.tmp matches 1 run return 0
execute unless entity @a[tag=npcraft.opponent,distance=..2.8,limit=1] run return 0
execute store result score #attack_at np.tmp run data get entity @s data.rival.attack_at
execute if score #now np.sys < #attack_at np.tmp run return 0
function npcraft:inventory/load
function npcraft:inventory/find_weapon
execute unless score #pick_slot np.tmp matches 0..35 run return 0
function npcraft:agent/show_pick with storage npcraft:inv pick
execute at @s run function npcraft:bot/sync with entity @s data
function npcraft:work/swing with entity @s data
# Dynamic damage is a server-chosen finite value, never a player-provided expression.
execute store result storage npcraft:scratch hit.damage int 1 run scoreboard players get #weapon_damage np.tmp
data modify storage npcraft:scratch hit.id set from entity @s data.id
function npcraft:rival/hit with storage npcraft:scratch hit
scoreboard players operation #attack_at np.tmp = #now np.sys
scoreboard players add #attack_at np.tmp 20
execute store result entity @s data.rival.attack_at int 1 run scoreboard players get #attack_at np.tmp
execute if score #hit_ok np.tmp matches 1 run function npcraft:actions/wear_pick with storage npcraft:inv pick
execute if score #hit_ok np.tmp matches 1 run function npcraft:inventory/commit
execute store result score #enemy_health np.tmp run data get entity @a[tag=npcraft.opponent,limit=1] Health
execute unless score #enemy_health np.tmp matches 1.. run function npcraft:rival/finish
