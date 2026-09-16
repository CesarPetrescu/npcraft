$execute store success score #ag_changed np.tmp run data modify entity @s data.agent.intent set value "$(name)"
execute if score #ag_changed np.tmp matches 1 run data remove entity @s data.target
execute if score #ag_changed np.tmp matches 1 run scoreboard players set @s np.dig 0
execute if score #ag_changed np.tmp matches 1 run data modify entity @s data.agent.failures set value 0
execute if score #ag_changed np.tmp matches 1 run data modify entity @s data.scan set value 0
execute if score #ag_changed np.tmp matches 1 run data modify entity @s data.scanned set value 0
execute if score #ag_changed np.tmp matches 1 run data remove entity @s data.navigation
