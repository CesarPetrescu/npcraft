# Native health, capped at the alpha's 20 HP. Meal healing is intentionally simplified.
$execute store result score #health np.tmp run data get entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)},limit=1] Health 100
scoreboard players add #health np.tmp 200
execute if score #health np.tmp matches 2001.. run scoreboard players set #health np.tmp 2000
$execute store result entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)},limit=1] Health float 0.01 run scoreboard players get #health np.tmp
