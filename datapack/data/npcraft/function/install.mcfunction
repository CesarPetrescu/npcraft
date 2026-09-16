scoreboard objectives add npcraft trigger
scoreboard objectives add np.id dummy
scoreboard objectives add np.owner dummy
scoreboard objectives add np.sel dummy
scoreboard objectives add np.count dummy
scoreboard objectives add np.mode dummy
scoreboard objectives add np.status dummy
scoreboard objectives add np.next dummy
scoreboard objectives add np.dig dummy
scoreboard objectives add np.depth dummy
scoreboard objectives add np.harvest dummy
scoreboard objectives add np.tmp dummy
scoreboard objectives add np.sys dummy
scoreboard players set #next np.sys 0
scoreboard players set #owners np.sys 0
scoreboard players set #total np.sys 0
scoreboard players set #enabled np.sys 1
data modify storage npcraft:state queue set value []
data modify storage npcraft:meta schema set value 1
data modify storage npcraft:meta installed set value 1b
