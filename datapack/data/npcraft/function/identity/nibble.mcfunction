scoreboard players operation #hex_nibble np.tmp = #hex_value np.tmp
scoreboard players operation #hex_nibble np.tmp %= #hex_base np.tmp
scoreboard players operation #hex_value np.tmp /= #hex_base np.tmp
scoreboard players set #hex_complement np.tmp 15
scoreboard players operation #hex_complement np.tmp -= #hex_nibble np.tmp
execute if score #hex_invert np.tmp matches 1 run scoreboard players operation #hex_nibble np.tmp = #hex_complement np.tmp
execute store result storage npcraft:uuid digit.index int 1 run scoreboard players get #hex_nibble np.tmp
function npcraft:identity/digit with storage npcraft:uuid digit
scoreboard players remove #hex_digits np.tmp 1
execute if score #hex_digits np.tmp matches 1.. run function npcraft:identity/nibble
