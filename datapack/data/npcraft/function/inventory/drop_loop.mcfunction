$execute if data entity @s data.inventory.slots[$(slot)].item run function npcraft:inventory/drop_slot {slot:$(slot)}
$scoreboard players set #iv_cursor np.tmp $(slot)
scoreboard players add #iv_cursor np.tmp 1
execute store result storage npcraft:inv cursor.slot int 1 run scoreboard players get #iv_cursor np.tmp
execute if score #iv_cursor np.tmp matches ..35 run function npcraft:inventory/drop_loop with storage npcraft:inv cursor
