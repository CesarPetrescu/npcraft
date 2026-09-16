$execute store result score #hex_value np.tmp run data get storage npcraft:uuid parts[$(index)]
scoreboard players set #hex_invert np.tmp 0
execute if score #hex_value np.tmp matches ..-1 run scoreboard players set #hex_invert np.tmp 1
scoreboard players set #hex_positive np.tmp -1
scoreboard players operation #hex_positive np.tmp -= #hex_value np.tmp
execute if score #hex_invert np.tmp matches 1 run scoreboard players operation #hex_value np.tmp = #hex_positive np.tmp
data modify storage npcraft:uuid word set value ""
scoreboard players set #hex_digits np.tmp 8
function npcraft:identity/nibble
data modify storage npcraft:uuid words append from storage npcraft:uuid word
$scoreboard players set #word_index np.tmp $(index)
scoreboard players add #word_index np.tmp 1
execute store result storage npcraft:uuid cursor.index int 1 run scoreboard players get #word_index np.tmp
execute if score #word_index np.tmp matches ..3 run function npcraft:identity/word with storage npcraft:uuid cursor
