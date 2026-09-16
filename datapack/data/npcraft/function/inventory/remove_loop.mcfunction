execute if score #iv_need np.tmp matches 0 run return 1
$execute if data storage npcraft:inv slots[$(slot)].item run function npcraft:inventory/remove_slot {slot:$(slot),kind:"$(kind)"}
$scoreboard players set #iv_cursor np.tmp $(slot)
scoreboard players add #iv_cursor np.tmp 1
execute store result storage npcraft:inv cursor.slot int 1 run scoreboard players get #iv_cursor np.tmp
$data modify storage npcraft:inv cursor.kind set value "$(kind)"
execute if score #iv_cursor np.tmp matches ..35 run function npcraft:inventory/remove_loop with storage npcraft:inv cursor
