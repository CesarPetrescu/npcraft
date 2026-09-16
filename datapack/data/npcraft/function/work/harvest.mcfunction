execute unless data entity @s data.tool run return 0
scoreboard players set #cargo np.tmp 0
execute store result score #cargo np.tmp run data get entity @s data.cargo.count
execute if score #cargo np.tmp matches 64.. run return 0
execute unless function npcraft:work/in_bounds run return run function npcraft:work/invalidate
function npcraft:work/sight with entity @s data.target
execute unless score #visible np.tmp matches 1 run return run scoreboard players set @s np.status 9
scoreboard players set @s np.status 3
function npcraft:work/swing with entity @s data
execute unless score @s np.dig matches 1.. run function npcraft:work/start_cut
execute if score #now np.sys < @s np.dig run return 0
function npcraft:work/commit with entity @s data.target
