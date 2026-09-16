execute if score #iv_left np.tmp matches 0 run return 1
$execute unless data storage npcraft:inv slots[$(slot)].item run function npcraft:inventory/empty_slot {slot:$(slot)}
$scoreboard players set #iv_cursor np.tmp $(slot)
scoreboard players add #iv_cursor np.tmp 1
execute store result storage npcraft:inv cursor.slot int 1 run scoreboard players get #iv_cursor np.tmp
execute if score #iv_cursor np.tmp matches ..35 run function npcraft:inventory/empty with storage npcraft:inv cursor
