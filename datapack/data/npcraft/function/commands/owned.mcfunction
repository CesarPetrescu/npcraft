# Called only after owner ID AND UUID authorization. All mutations are local to this controller.
# Reject unknown actions before touching the controller or pending action.
execute unless score #cmd np.tmp matches 4..16 unless score #cmd np.tmp matches 20..25 unless score #cmd np.tmp matches 99 run return 0
function npcraft:agent/init
execute if score #cmd np.tmp matches 20 run return run dialog show @a[tag=npcraft.actor] npcraft:agent
execute if score #cmd np.tmp matches 21 run function npcraft:inventory/give
execute if score #cmd np.tmp matches 22 run scoreboard players set @s np.mode 0
execute if score #cmd np.tmp matches 22 run function npcraft:actions/result {state:"cancelled",reason:"backpack_returned"}
execute if score #cmd np.tmp matches 22 run function npcraft:inventory/drop
execute if score #cmd np.tmp matches 23 run function npcraft:agent/start
execute if score #cmd np.tmp matches 24 run function npcraft:agent/set_bench
execute if score #cmd np.tmp matches 25 run return run function npcraft:agent/status
execute if score #cmd np.tmp matches 4 run scoreboard players set @s np.mode 1
execute if score #cmd np.tmp matches 5 run scoreboard players set @s np.mode 0
execute if score #cmd np.tmp matches 6 run function npcraft:commands/set_home
execute if score #cmd np.tmp matches 7 run scoreboard players set @s np.mode 2
execute if score #cmd np.tmp matches 8 run function npcraft:commands/set_plot
execute if score #cmd np.tmp matches 9 run function npcraft:commands/set_storage
execute if score #cmd np.tmp matches 10 run scoreboard players set @s np.mode 3
execute if score #cmd np.tmp matches 11 run scoreboard players set @s np.mode 0
execute if score #cmd np.tmp matches 11 run function npcraft:actions/result {state:"cancelled",reason:"owner_stop"}
execute if score #cmd np.tmp matches 12 run return run dialog show @a[tag=npcraft.actor] npcraft:dismiss
execute if score #cmd np.tmp matches 13 run return run function npcraft:commands/status
execute if score #cmd np.tmp matches 14 run function npcraft:commands/equip
execute if score #cmd np.tmp matches 15 run function npcraft:commands/drop_tool
execute if score #cmd np.tmp matches 16 run function npcraft:commands/drop_cargo
execute if score #cmd np.tmp matches 99 run return run function npcraft:commands/dismiss with entity @s data
# Orders invalidate pending harvests. Revalidation is mandatory after any change.
data remove entity @s data.target
scoreboard players set @s np.dig 0
scoreboard players set @s np.next 0
