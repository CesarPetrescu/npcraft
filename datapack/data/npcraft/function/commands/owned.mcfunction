# Called only after owner ID AND UUID authorization. All mutations are local to this controller.
execute if score #cmd np.tmp matches 4 run scoreboard players set @s np.mode 1
execute if score #cmd np.tmp matches 5 run scoreboard players set @s np.mode 0
execute if score #cmd np.tmp matches 6 run function npcraft:commands/set_home
execute if score #cmd np.tmp matches 7 run scoreboard players set @s np.mode 2
execute if score #cmd np.tmp matches 8 run function npcraft:commands/set_plot
execute if score #cmd np.tmp matches 9 run function npcraft:commands/set_storage
execute if score #cmd np.tmp matches 10 run scoreboard players set @s np.mode 3
execute if score #cmd np.tmp matches 11 run scoreboard players set @s np.mode 0
execute if score #cmd np.tmp matches 12 run dialog show @a[tag=npcraft.actor] npcraft:dismiss
execute if score #cmd np.tmp matches 13 run function npcraft:commands/status
execute if score #cmd np.tmp matches 14 run function npcraft:commands/equip
execute if score #cmd np.tmp matches 15 run function npcraft:commands/drop_tool
execute if score #cmd np.tmp matches 16 run function npcraft:commands/drop_cargo
execute if score #cmd np.tmp matches 20..25 run function npcraft:agent/commands
execute if score #cmd np.tmp matches 4..11 if data entity @s data.agent run function npcraft:agent/invalidate
execute if score #cmd np.tmp matches 99 run return run function npcraft:commands/dismiss with entity @s data
# Read-only views must not reset work deadlines or discard an in-flight target.
execute if score #cmd np.tmp matches 12..13 run return 0
execute if score #cmd np.tmp matches 20 run return 0
execute if score #cmd np.tmp matches 24 run return 0
# Behavior/inventory changes invalidate pending harvests and wake the controller.
data remove entity @s data.target
scoreboard players set @s np.dig 0
scoreboard players set @s np.next 0
