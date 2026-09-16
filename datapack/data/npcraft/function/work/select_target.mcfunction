$data modify entity @s data.target set value {x:$(x),y:$(y),z:$(z),kind:"$(kind)"}
data modify entity @s data.scanned set value 0
scoreboard players set @s np.dig 0
