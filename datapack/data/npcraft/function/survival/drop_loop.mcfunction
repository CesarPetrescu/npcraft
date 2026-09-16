$execute if data entity @s data.inventory.slots[$(slot)].item run function npcraft:survival/drop_slot {slot:$(slot)}
$scoreboard players set #drop_cursor np.tmp $(slot)
scoreboard players add #drop_cursor np.tmp 1
execute store result storage npcraft:scratch drop_cursor.slot int 1 run scoreboard players get #drop_cursor np.tmp
execute if score #drop_cursor np.tmp matches ..35 run function npcraft:survival/drop_loop with storage npcraft:scratch drop_cursor
