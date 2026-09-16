$data remove storage npcraft:state consents[{id:$(id)}]
$execute in minecraft:overworld as @e[type=minecraft:marker,tag=npcraft.bot,scores={np.owner=$(id)}] at @s if data entity @s data.rival{enabled:1b} run function npcraft:rival/stop
