$execute store result entity @s data.dest.x int 1 run data get entity @a[distance=..64,scores={np.owner=$(owner)},limit=1] Pos[0]
$execute store result entity @s data.dest.y int 1 run data get entity @a[distance=..64,scores={np.owner=$(owner)},limit=1] Pos[1]
$execute store result entity @s data.dest.z int 1 run data get entity @a[distance=..64,scores={np.owner=$(owner)},limit=1] Pos[2]
data modify entity @s data.dest.range set value 2
function npcraft:nav/plan
