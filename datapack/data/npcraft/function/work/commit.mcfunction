# Only oak/birch logs are supported: their unenchanted vanilla drop is exactly one log.
# No destroy drops are produced; successful removal precedes inventory credit.
$execute unless block $(x) $(y) $(z) $(kind) run return run function npcraft:work/invalidate
execute unless function npcraft:work/in_bounds run return run function npcraft:work/invalidate
$execute if data entity @s data.cargo unless data entity @s data.cargo{id:"$(kind)"} run return 0
scoreboard players set #cargo np.tmp 0
execute store result score #cargo np.tmp run data get entity @s data.cargo.count
execute if score #cargo np.tmp matches 64.. run return 0
execute unless data entity @s data.tool run return 0
$execute store success score #broke np.tmp run setblock $(x) $(y) $(z) minecraft:air
execute unless score #broke np.tmp matches 1 run return 0
scoreboard players add #cargo np.tmp 1
$data modify entity @s data.cargo set value {id:"$(kind)",count:1}
execute store result entity @s data.cargo.count int 1 run scoreboard players get #cargo np.tmp
scoreboard players set #damage np.tmp 0
execute store result score #damage np.tmp run data get entity @s data.tool.components."minecraft:damage"
scoreboard players add #damage np.tmp 1
execute store result entity @s data.tool.components."minecraft:damage" int 1 run scoreboard players get #damage np.tmp
execute if score #damage np.tmp matches 250.. run data remove entity @s data.tool
scoreboard players add @s np.harvest 1
function npcraft:work/invalidate
