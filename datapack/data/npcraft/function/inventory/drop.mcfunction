function npcraft:agent/init
# Per-slot success checks preserve unsummoned items. Drops are public, not private.
function npcraft:inventory/drop_loop {slot:0}
data remove entity @s data.agent.display
function npcraft:bot/sync with entity @s data
