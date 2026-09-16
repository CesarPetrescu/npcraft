# Shared usable-tool predicate for planning, actions, and equipped presentation.
scoreboard players set #pick_slot np.tmp -1
scoreboard players set #pick_best np.tmp 0
function npcraft:inventory/pick_loop {slot:0}
