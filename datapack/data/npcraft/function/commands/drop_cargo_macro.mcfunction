$execute store success score #dropped np.tmp run summon minecraft:item ~ ~0.5 ~ {Item:$(cargo),PickupDelay:0s}
execute if score #dropped np.tmp matches 1 run data remove entity @s data.cargo
