# Additive, lazy migration: legacy tool/cargo/owner/schema remain untouched.
execute unless data entity @s data.inventory run data modify entity @s data.inventory set value {version:1,slots:[{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]}
execute unless data entity @s data.agent run data modify entity @s data.agent set value {version:1,intent:"idle",state:"idle",reason:"none",failures:0,blocked:[],blocked_until:0}
