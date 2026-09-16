# Fixed, auditable dependency graph, not arbitrary language-model actions.
execute if score #pg_bench np.tmp matches 0 run return run function npcraft:progression/need_bench
execute if score #pg_pick np.tmp matches ..130 run return run function npcraft:agent/plan
execute if score #pg_pick np.tmp matches 250.. unless data entity @s data.agent{goal:"rival_kit"} run return run function npcraft:agent/intent {name:"iron_complete"}
execute if score #pg_pick np.tmp matches 250.. if score #pg_sword np.tmp matches 1.. run return run function npcraft:agent/intent {name:"kit_complete"}
scoreboard players set #pg_need np.tmp 3
execute if score #pg_pick np.tmp matches 250.. run scoreboard players set #pg_need np.tmp 2
execute if score #pg_iron np.tmp >= #pg_need np.tmp run return run function npcraft:progression/need_final_recipe
execute if score #pg_station np.tmp matches 0 run return run function npcraft:progression/need_furnace
execute if score #pg_output np.tmp matches 1.. run return run function npcraft:agent/intent {name:"smelt"}
execute if score #pg_stock np.tmp < #pg_need np.tmp run return run function npcraft:agent/intent {name:"mine_iron"}
execute if score #pg_coal np.tmp matches 0 if score #pg_fuel np.tmp matches 0 if score #pg_lit np.tmp matches 0 run return run function npcraft:agent/intent {name:"mine_coal"}
function npcraft:agent/intent {name:"smelt"}
