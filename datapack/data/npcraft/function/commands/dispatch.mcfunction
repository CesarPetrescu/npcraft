scoreboard players operation #cmd np.tmp = @s npcraft
scoreboard players set @s npcraft 0
execute if score #cmd np.tmp matches 1 run return run function npcraft:help
execute if score #cmd np.tmp matches 42 run return run function npcraft:commands/end_rivals
execute unless entity @s[tag=npcraft.allowed] run return run tellraw @s {"text":"Ask an operator to grant NPCraft access first.","color":"red"}
execute unless score #enabled np.sys matches 1 run return run tellraw @s {"text":"NPCraft is paused by an operator.","color":"yellow"}
execute unless dimension minecraft:overworld run return run tellraw @s {"text":"This alpha supports the Overworld only.","color":"yellow"}
tag @a remove npcraft.actor
tag @s add npcraft.actor
scoreboard players operation #actor np.tmp = @s np.owner
execute if score #cmd np.tmp matches 2 run function npcraft:commands/recruit
execute if score #cmd np.tmp matches 3 run function npcraft:commands/select
execute if score #cmd np.tmp matches 4..99 run function npcraft:commands/route
tag @s remove npcraft.actor
