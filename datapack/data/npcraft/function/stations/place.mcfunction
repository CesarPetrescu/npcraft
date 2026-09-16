scoreboard players set #place_done np.tmp 0
$execute positioned ~1 ~ ~ run function npcraft:stations/candidate {kind:"$(kind)",key:"$(key)"}
$execute if score #place_done np.tmp matches 0 positioned ~-1 ~ ~ run function npcraft:stations/candidate {kind:"$(kind)",key:"$(key)"}
$execute if score #place_done np.tmp matches 0 positioned ~ ~ ~1 run function npcraft:stations/candidate {kind:"$(kind)",key:"$(key)"}
$execute if score #place_done np.tmp matches 0 positioned ~ ~ ~-1 run function npcraft:stations/candidate {kind:"$(kind)",key:"$(key)"}
$execute if score #place_done np.tmp matches 0 positioned ~1 ~-1 ~ run function npcraft:stations/candidate {kind:"$(kind)",key:"$(key)"}
$execute if score #place_done np.tmp matches 0 positioned ~-1 ~-1 ~ run function npcraft:stations/candidate {kind:"$(kind)",key:"$(key)"}
$execute if score #place_done np.tmp matches 0 positioned ~ ~-1 ~1 run function npcraft:stations/candidate {kind:"$(kind)",key:"$(key)"}
$execute if score #place_done np.tmp matches 0 positioned ~ ~-1 ~-1 run function npcraft:stations/candidate {kind:"$(kind)",key:"$(key)"}
execute if score #place_done np.tmp matches 0 run function npcraft:actions/result {state:"blocked",reason:"no_safe_station_space"}
