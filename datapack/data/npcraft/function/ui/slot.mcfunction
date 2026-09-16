$execute if data entity @s data.inventory.slots[$(slot)].item run function npcraft:ui/row {slot:$(slot)}
$scoreboard players set #ui_cursor np.tmp $(slot)
scoreboard players add #ui_cursor np.tmp 1
execute store result storage npcraft:scratch ui_cursor.slot int 1 run scoreboard players get #ui_cursor np.tmp
execute if score #ui_cursor np.tmp matches ..35 run function npcraft:ui/slot with storage npcraft:scratch ui_cursor
