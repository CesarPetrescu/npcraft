# Direct UUID lookup includes a dying entity that @e's living filter can no longer select.
$execute unless entity $(body_uuid) run return run function npcraft:survival/died
$execute store result score #native_health np.tmp run data get entity $(body_uuid) Health 100
execute store result entity @s data.survival.health float 0.01 run scoreboard players get #native_health np.tmp
# 26.3 mannequins cannot serialize the native DYING pose. Retire it without reviving it.
$execute if score #native_health np.tmp matches ..0 run data merge entity $(body_uuid) {pose:"standing",DeathTime:19s}
execute if score #native_health np.tmp matches ..0 run function npcraft:survival/died
