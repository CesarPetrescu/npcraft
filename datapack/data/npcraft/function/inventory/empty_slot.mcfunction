$data modify storage npcraft:inv slots[$(slot)] set from storage npcraft:inv input
$execute store result storage npcraft:inv slots[$(slot)].item.count int 1 run scoreboard players get #iv_left np.tmp
scoreboard players set #iv_left np.tmp 0
