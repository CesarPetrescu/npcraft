$data modify storage npcraft:inv current set from storage npcraft:inv slots[$(slot)].item
$function npcraft:inventory/match {kind:"$(kind)"}
execute unless score #iv_match np.tmp matches 1 run return 0
execute store result score #iv_count np.tmp run data get storage npcraft:inv current.count
scoreboard players operation #iv_take np.tmp = #iv_count np.tmp
scoreboard players operation #iv_take np.tmp < #iv_need np.tmp
scoreboard players operation #iv_need np.tmp -= #iv_take np.tmp
scoreboard players operation #iv_count np.tmp -= #iv_take np.tmp
$execute store result storage npcraft:inv slots[$(slot)].item.count int 1 run scoreboard players get #iv_count np.tmp
$execute if score #iv_count np.tmp matches 0 run data modify storage npcraft:inv slots[$(slot)] set value {}
