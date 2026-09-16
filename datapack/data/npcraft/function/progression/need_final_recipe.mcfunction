execute if score #ag_sticks np.tmp matches ..1 if score #ag_planks np.tmp matches 2.. run return run function npcraft:agent/intent {name:"craft_sticks"}
execute if score #ag_sticks np.tmp matches ..1 run return run function npcraft:progression/need_wood
execute if score #pg_pick np.tmp matches 250.. run return run function npcraft:agent/intent {name:"craft_iron_sword"}
function npcraft:agent/intent {name:"craft_iron_pick"}
