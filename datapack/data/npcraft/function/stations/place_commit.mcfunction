# Closed kind/key pair, exact permission bounds and live reach at the mutation boundary.
$data modify storage npcraft:scratch pair set value {kind:"$(kind)",key:"$(key)"}
execute unless data storage npcraft:scratch pair{kind:"minecraft:crafting_table",key:"bench"} unless data storage npcraft:scratch pair{kind:"minecraft:furnace",key:"furnace"} run return 0
$data modify entity @s data.target set value {x:$(x),y:$(y),z:$(z),kind:"$(kind)"}
execute unless function npcraft:work/in_bounds run return 0
$execute positioned $(x) $(y) $(z) align xyz positioned ~0.5 ~ ~0.5 unless entity @s[distance=..2] run return 0
$execute positioned $(x) $(y) $(z) unless function npcraft:nav/cell_safe run return 0
$execute unless block $(x) $(y) $(z) minecraft:air run return 0
$execute positioned $(x) $(y) $(z) align xyz if entity @e[type=!minecraft:marker,dx=0,dy=0,dz=0] run return 0
function npcraft:inventory/load
$function npcraft:inventory/remove {kind:"$(kind)",count:1}
execute unless score #inv_ok np.tmp matches 1 run return 0
$execute store success score #placed np.tmp run setblock $(x) $(y) $(z) $(kind)
execute unless score #placed np.tmp matches 1 run return 0
function npcraft:inventory/commit
$data modify entity @s data.agent.$(key) set value {x:$(x),y:$(y),z:$(z),owned:1b}
$execute if block $(x) $(y) $(z) minecraft:furnace run data modify block $(x) $(y) $(z) CustomName set value {text:"NPCraft furnace #$(id)"}
$execute if block $(x) $(y) $(z) minecraft:furnace run data modify entity @s data.agent.furnace.name set from block $(x) $(y) $(z) CustomName
scoreboard players set #place_done np.tmp 1
function npcraft:work/invalidate
function npcraft:actions/result {state:"succeeded",reason:"station_placed"}
