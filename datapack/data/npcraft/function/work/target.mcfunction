$execute unless block $(x) $(y) $(z) $(kind) run return run function npcraft:work/invalidate
execute unless function npcraft:work/in_bounds run return run function npcraft:work/invalidate
$execute if data entity @s data.cargo unless data entity @s data.cargo{id:"$(kind)"} run return run function npcraft:work/deposit
data modify entity @s data.dest set from entity @s data.target
data modify entity @s data.dest.y set from entity @s data.plot.y
data modify entity @s data.dest.range set value 1
function npcraft:nav/plan
execute unless score #arrived np.tmp matches 1 run return 0
function npcraft:work/harvest
