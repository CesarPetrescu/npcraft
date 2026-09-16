execute unless data entity @s data.plot run return 0
execute store result score #dx np.tmp run data get entity @s data.target.x
execute store result score #dy np.tmp run data get entity @s data.target.y
execute store result score #dz np.tmp run data get entity @s data.target.z
execute store result score #x np.tmp run data get entity @s data.plot.x
execute store result score #y np.tmp run data get entity @s data.plot.y
execute store result score #z np.tmp run data get entity @s data.plot.z
scoreboard players operation #dx np.tmp -= #x np.tmp
scoreboard players operation #dy np.tmp -= #y np.tmp
scoreboard players operation #dz np.tmp -= #z np.tmp
execute unless score #dx np.tmp matches -3..3 run return 0
execute unless score #dz np.tmp matches -3..3 run return 0
execute unless score #dy np.tmp matches 0..3 run return 0
return 1
