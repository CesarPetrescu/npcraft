execute if data entity @s data.survival{dead:1b} run return run function npcraft:survival/dead_tick
execute unless data entity @s data.survival.body_uuid run function npcraft:survival/remember_body with entity @s data
execute if data entity @s data.survival.body_uuid run function npcraft:survival/read_health with entity @s data
execute if data entity @s data.survival{dead:1b} run return 0
execute unless score #enabled np.sys matches 1 run return 0
scoreboard players set #survival_at np.tmp 0
execute store result score #survival_at np.tmp run data get entity @s data.survival.next
execute if score #now np.sys < #survival_at np.tmp run return 0
scoreboard players operation #survival_at np.tmp = #now np.sys
scoreboard players add #survival_at np.tmp 20
execute store result entity @s data.survival.next int 1 run scoreboard players get #survival_at np.tmp
execute store result score #food np.tmp run data get entity @s data.survival.food
execute store result score #hunger_at np.tmp run data get entity @s data.survival.hunger_at
execute if score #now np.sys >= #hunger_at np.tmp run function npcraft:survival/hunger
execute store result score #health np.tmp run data get entity @s data.survival.health
execute if score #food np.tmp matches ..14 run function npcraft:survival/eat with entity @s data
execute if score #health np.tmp matches ..16 run function npcraft:survival/eat with entity @s data
execute if score #food np.tmp matches 0 run function npcraft:survival/starve with entity @s data
