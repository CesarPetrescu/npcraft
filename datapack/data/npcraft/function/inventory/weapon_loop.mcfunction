$execute if data storage npcraft:inv slots[$(slot)].item{id:"minecraft:wooden_sword"} run function npcraft:inventory/pick_check {slot:$(slot),kind:"minecraft:wooden_sword",durability:59}
$execute if data storage npcraft:inv slots[$(slot)].item{id:"minecraft:stone_sword"} run function npcraft:inventory/pick_check {slot:$(slot),kind:"minecraft:stone_sword",durability:131}
$execute if data storage npcraft:inv slots[$(slot)].item{id:"minecraft:iron_sword"} run function npcraft:inventory/pick_check {slot:$(slot),kind:"minecraft:iron_sword",durability:250}
$scoreboard players set #weapon_cursor np.tmp $(slot)
scoreboard players add #weapon_cursor np.tmp 1
execute store result storage npcraft:inv cursor.slot int 1 run scoreboard players get #weapon_cursor np.tmp
execute if score #weapon_cursor np.tmp matches ..35 run function npcraft:inventory/weapon_loop with storage npcraft:inv cursor
