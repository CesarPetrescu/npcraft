# Finite, deterministic dependency planner. No claims of general GOAP/LLM reasoning.
# Priority: fulfilled goal > ready final recipe > tool prerequisite > stone > sticks > planks > logs.
execute if score #ag_stone_pick np.tmp matches 1.. run return run function npcraft:agent/intent {name:"complete"}
execute if score #ag_cobble np.tmp matches 3.. if score #ag_sticks np.tmp matches 2.. run return run function npcraft:agent/intent {name:"craft_stone_pick"}
execute if score #ag_wood_pick np.tmp matches 0 if score #ag_planks np.tmp matches 3.. if score #ag_sticks np.tmp matches 2.. run return run function npcraft:agent/intent {name:"craft_wood_pick"}
execute if score #ag_wood_pick np.tmp matches 1.. if score #ag_cobble np.tmp matches ..2 run return run function npcraft:agent/intent {name:"mine_stone"}
execute if score #ag_sticks np.tmp matches ..1 if score #ag_planks np.tmp matches 2.. run return run function npcraft:agent/intent {name:"craft_sticks"}
execute if score #ag_logs np.tmp matches 1.. run return run function npcraft:agent/intent {name:"craft_planks"}
function npcraft:agent/intent {name:"gather_logs"}
