scoreboard players set #recovering np.tmp 0
execute unless data entity @s data.survival.recover run return 0
execute store result score #recover_until np.tmp run data get entity @s data.survival.recover_until
execute if score #now np.sys >= #recover_until np.tmp run return run data remove entity @s data.survival.recover
scoreboard players set #recovering np.tmp 1
function npcraft:survival/pickup with entity @s data
execute if score #pickup_ok np.tmp matches 1 run return 0
data modify entity @s data.dest set from entity @s data.survival.recover
data modify entity @s data.dest.range set value 1
function npcraft:nav/plan
execute if score #arrived np.tmp matches 1 run data remove entity @s data.survival.recover
