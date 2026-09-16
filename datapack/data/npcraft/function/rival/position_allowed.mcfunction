# Common box policy: +/-16 X/Z, +/-8 Y from immutable duel center.
scoreboard players set #arena_ok np.tmp 0
execute store result score #arena_x np.tmp run data get storage npcraft:scratch arena_pos.x
execute store result score #arena_y np.tmp run data get storage npcraft:scratch arena_pos.y
execute store result score #arena_z np.tmp run data get storage npcraft:scratch arena_pos.z
execute store result score #center_x np.tmp run data get entity @s data.rival.center.x
execute store result score #center_y np.tmp run data get entity @s data.rival.center.y
execute store result score #center_z np.tmp run data get entity @s data.rival.center.z
scoreboard players operation #arena_x np.tmp -= #center_x np.tmp
scoreboard players operation #arena_y np.tmp -= #center_y np.tmp
scoreboard players operation #arena_z np.tmp -= #center_z np.tmp
execute if score #arena_x np.tmp matches -16..16 if score #arena_y np.tmp matches -8..8 if score #arena_z np.tmp matches -16..16 run scoreboard players set #arena_ok np.tmp 1
