scoreboard players set #eat_at np.tmp 0
execute store result score #eat_at np.tmp run data get entity @s data.survival.eat_at
execute if score #now np.sys < #eat_at np.tmp run return 0
function npcraft:inventory/load
function npcraft:inventory/count {kind:"minecraft:cooked_beef"}
execute if score #iv_total np.tmp matches 1.. run return run function npcraft:survival/consume {kind:"minecraft:cooked_beef",food:8}
function npcraft:inventory/count {kind:"minecraft:bread"}
execute if score #iv_total np.tmp matches 1.. run return run function npcraft:survival/consume {kind:"minecraft:bread",food:5}
function npcraft:inventory/count {kind:"minecraft:apple"}
execute if score #iv_total np.tmp matches 1.. run return run function npcraft:survival/consume {kind:"minecraft:apple",food:4}
function npcraft:actions/result {state:"blocked",reason:"need_food_supply"}
