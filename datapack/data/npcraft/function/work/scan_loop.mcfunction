execute if data entity @s data.target run return 1
execute unless score #scan_budget np.tmp matches 1.. run return 0
scoreboard players remove #scan_budget np.tmp 1
scoreboard players set #scanned np.tmp 0
execute store result score #scanned np.tmp run data get entity @s data.scanned
execute if score #scanned np.tmp matches ..195 run scoreboard players add #scanned np.tmp 1
execute store result entity @s data.scanned int 1 run scoreboard players get #scanned np.tmp
execute store result score #index np.tmp run data get entity @s data.scan
scoreboard players set #seven np.tmp 7
scoreboard players set #fortynine np.tmp 49
scoreboard players operation #dx np.tmp = #index np.tmp
scoreboard players operation #dx np.tmp %= #seven np.tmp
scoreboard players remove #dx np.tmp 3
scoreboard players operation #dz np.tmp = #index np.tmp
scoreboard players operation #dz np.tmp /= #seven np.tmp
scoreboard players operation #dz np.tmp %= #seven np.tmp
scoreboard players remove #dz np.tmp 3
scoreboard players operation #dy np.tmp = #index np.tmp
scoreboard players operation #dy np.tmp /= #fortynine np.tmp
execute store result score #x np.tmp run data get entity @s data.plot.x
execute store result score #y np.tmp run data get entity @s data.plot.y
execute store result score #z np.tmp run data get entity @s data.plot.z
scoreboard players operation #x np.tmp += #dx np.tmp
scoreboard players operation #y np.tmp += #dy np.tmp
scoreboard players operation #z np.tmp += #dz np.tmp
execute store result storage npcraft:scratch candidate.x int 1 run scoreboard players get #x np.tmp
execute store result storage npcraft:scratch candidate.y int 1 run scoreboard players get #y np.tmp
execute store result storage npcraft:scratch candidate.z int 1 run scoreboard players get #z np.tmp
scoreboard players add #index np.tmp 1
execute if score #index np.tmp matches 196.. run scoreboard players set #index np.tmp 0
execute store result entity @s data.scan int 1 run scoreboard players get #index np.tmp
function npcraft:work/candidate with storage npcraft:scratch candidate
function npcraft:work/scan_loop
