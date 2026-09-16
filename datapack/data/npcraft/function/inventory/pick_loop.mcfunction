$execute if data storage npcraft:inv slots[$(slot)].item{id:"minecraft:wooden_pickaxe"} run function npcraft:inventory/pick_check {slot:$(slot),kind:"minecraft:wooden_pickaxe",durability:59}
$execute if data storage npcraft:inv slots[$(slot)].item{id:"minecraft:stone_pickaxe"} run function npcraft:inventory/pick_check {slot:$(slot),kind:"minecraft:stone_pickaxe",durability:131}
$execute if data storage npcraft:inv slots[$(slot)].item{id:"minecraft:iron_pickaxe"} run function npcraft:inventory/pick_check {slot:$(slot),kind:"minecraft:iron_pickaxe",durability:250}
$scoreboard players set #iv_cursor np.tmp $(slot)
scoreboard players add #iv_cursor np.tmp 1
execute store result storage npcraft:inv cursor.slot int 1 run scoreboard players get #iv_cursor np.tmp
execute if score #iv_cursor np.tmp matches ..35 run function npcraft:inventory/pick_loop with storage npcraft:inv cursor
