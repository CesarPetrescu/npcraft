$data modify storage npcraft:inv current set from storage npcraft:inv slots[$(slot)].item
$function npcraft:inventory/match {kind:"$(kind)"}
execute unless score #iv_match np.tmp matches 1 run return 0
execute store result score #iv_count np.tmp run data get storage npcraft:inv current.count
scoreboard players operation #iv_total np.tmp += #iv_count np.tmp
