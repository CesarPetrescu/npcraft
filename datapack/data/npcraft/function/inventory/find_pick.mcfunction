# Usable tools deliberately restricted to plain wooden/stone picks (optional damage).
# Named/enchanted/custom-component items may be stored but are not silently emulated.
scoreboard players set #pick_slot np.tmp -1
scoreboard players set #pick_best np.tmp 0
function npcraft:inventory/pick_loop {slot:0}
