execute unless data entity @s data.plot run return run scoreboard players set @s np.status 7
execute unless data entity @s data.storage run return run scoreboard players set @s np.status 8
scoreboard players set #cargo np.tmp 0
execute store result score #cargo np.tmp run data get entity @s data.cargo.count
execute if score #cargo np.tmp matches 64.. run return run function npcraft:work/deposit
execute if data entity @s data.cargo unless data entity @s data.tool run return run function npcraft:work/deposit
execute unless data entity @s data.tool run return run scoreboard players set @s np.status 6
execute unless data entity @s data.target run function npcraft:work/scan
execute unless data entity @s data.target if data entity @s data.cargo if data entity @s data{scanned:196} run return run function npcraft:work/deposit
execute unless data entity @s data.target run return 0
function npcraft:work/target with entity @s data.target
