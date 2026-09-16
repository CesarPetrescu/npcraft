data modify entity @s data.dest set from entity @s data.home
data modify entity @s data.dest.range set value 0
function npcraft:nav/plan
execute if score #arrived np.tmp matches 1 run scoreboard players set @s np.mode 0
