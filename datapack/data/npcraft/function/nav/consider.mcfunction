execute store result score #nx np.tmp run data get entity @s Pos[0]
execute store result score #nz np.tmp run data get entity @s Pos[2]
scoreboard players operation #nx np.tmp -= #gx np.tmp
scoreboard players operation #nz np.tmp -= #gz np.tmp
execute if score #nx np.tmp matches ..-1 run scoreboard players operation #nx np.tmp *= #minus np.tmp
execute if score #nz np.tmp matches ..-1 run scoreboard players operation #nz np.tmp *= #minus np.tmp
scoreboard players operation #nx np.tmp += #nz np.tmp
execute unless score #nx np.tmp < #best np.tmp run return 0
scoreboard players operation #best np.tmp = #nx np.tmp
function npcraft:nav/found
