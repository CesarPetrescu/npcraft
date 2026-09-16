# Installation is idempotent. Do not reset IDs, records or a paused server on reload.
execute unless data storage npcraft:meta installed run function npcraft:install
execute unless data storage npcraft:meta {schema:1} run return 0
data modify storage npcraft:meta version set value "0.3.0-alpha.1"
execute in minecraft:overworld run function npcraft:nav/cleanup
say [NPCraft] 0.3.0-alpha.1 loaded (Java 26.3).
