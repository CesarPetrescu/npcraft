$execute store result score #iv_limit np.tmp run data get storage npcraft:inv slots[$(slot)].max
execute unless score #iv_limit np.tmp = #iv_max np.tmp run return 0
$data modify storage npcraft:inv compare set from storage npcraft:inv slots[$(slot)].item
data modify storage npcraft:inv compare.count set value 1
execute store success score #iv_different np.tmp run data modify storage npcraft:inv compare set from storage npcraft:inv key
execute unless score #iv_different np.tmp matches 0 run return 0
$execute store result score #iv_count np.tmp run data get storage npcraft:inv slots[$(slot)].item.count
scoreboard players operation #iv_room np.tmp = #iv_max np.tmp
scoreboard players operation #iv_room np.tmp -= #iv_count np.tmp
execute unless score #iv_room np.tmp matches 1.. run return 0
scoreboard players operation #iv_room np.tmp < #iv_left np.tmp
scoreboard players operation #iv_count np.tmp += #iv_room np.tmp
scoreboard players operation #iv_left np.tmp -= #iv_room np.tmp
$execute store result storage npcraft:inv slots[$(slot)].item.count int 1 run scoreboard players get #iv_count np.tmp
