scoreboard players set #iv_match np.tmp 0
$execute if data storage npcraft:inv current{id:"$(kind)"} run scoreboard players set #iv_match np.tmp 1
$data modify storage npcraft:inv kind set value "$(kind)"
execute if data storage npcraft:inv {kind:"logs"} if data storage npcraft:inv current{id:"minecraft:oak_log"} run scoreboard players set #iv_match np.tmp 1
execute if data storage npcraft:inv {kind:"logs"} if data storage npcraft:inv current{id:"minecraft:birch_log"} run scoreboard players set #iv_match np.tmp 1
execute if data storage npcraft:inv {kind:"planks"} if data storage npcraft:inv current{id:"minecraft:oak_planks"} run scoreboard players set #iv_match np.tmp 1
execute if data storage npcraft:inv {kind:"planks"} if data storage npcraft:inv current{id:"minecraft:birch_planks"} run scoreboard players set #iv_match np.tmp 1
