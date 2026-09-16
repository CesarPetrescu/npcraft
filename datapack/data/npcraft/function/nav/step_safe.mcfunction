$execute positioned $(x) $(y) $(z) unless function npcraft:nav/cell_safe run return 0
execute unless function npcraft:nav/cell_safe run return 0
execute store result score #sx np.tmp run data get entity @s Pos[0]
execute store result score #sy np.tmp run data get entity @s Pos[1]
execute store result score #sz np.tmp run data get entity @s Pos[2]
$data modify storage npcraft:nav landing set value {x:$(x),y:$(y),z:$(z)}
execute store result score #tx np.tmp run data get storage npcraft:nav landing.x
execute store result score #ty np.tmp run data get storage npcraft:nav landing.y
execute store result score #tz np.tmp run data get storage npcraft:nav landing.z
scoreboard players operation #tx np.tmp -= #sx np.tmp
scoreboard players operation #ty np.tmp -= #sy np.tmp
scoreboard players operation #tz np.tmp -= #sz np.tmp
scoreboard players set #negative np.tmp -1
execute if score #tx np.tmp matches ..-1 run scoreboard players operation #tx np.tmp *= #negative np.tmp
execute if score #tz np.tmp matches ..-1 run scoreboard players operation #tz np.tmp *= #negative np.tmp
scoreboard players operation #tx np.tmp += #tz np.tmp
execute unless score #tx np.tmp matches 1 run return 0
execute unless score #ty np.tmp matches -2..1 run return 0
execute if score #ty np.tmp matches 1 unless block ~ ~2 ~ #npcraft:clear run return 0
$execute if score #ty np.tmp matches -1 positioned $(x) $(y) $(z) unless block ~ ~2 ~ #npcraft:clear run return 0
$execute if score #ty np.tmp matches -2 positioned $(x) $(y) $(z) unless block ~ ~2 ~ #npcraft:clear run return 0
$execute if score #ty np.tmp matches -2 positioned $(x) $(y) $(z) unless block ~ ~3 ~ #npcraft:clear run return 0
$execute positioned $(x) $(y) $(z) if entity @e[type=minecraft:marker,tag=npcraft.bot,distance=..0.65] run return 0
execute if data entity @s data.rival{enabled:1b} run return run function npcraft:rival/step_allowed with storage npcraft:nav landing
return 1
