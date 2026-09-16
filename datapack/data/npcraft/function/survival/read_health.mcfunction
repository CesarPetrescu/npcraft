# Never NBT-serialize a dying mannequin: vanilla 26.3 cannot encode its DYING pose.
# @e excludes the native corpse; death is recorded without reading/modifying corpse NBT.
$execute unless entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)},limit=1] run return run function npcraft:survival/died
$execute store result score #native_health np.tmp run data get entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)},limit=1] Health 100
execute store result entity @s data.survival.health float 0.01 run scoreboard players get #native_health np.tmp
execute if score #native_health np.tmp matches ..0 run function npcraft:survival/died
