function npcraft:survival/drop_all
execute if data entity @s data.inventory.slots[].item run return 0
execute if data entity @s data.tool run return 0
execute if data entity @s data.cargo run return 0
execute unless score #enabled np.sys matches 1 run return 0
execute store result score #respawn_at np.tmp run data get entity @s data.survival.respawn_at
execute if score #now np.sys < #respawn_at np.tmp run return 0
execute unless data entity @s data.home run return 0
function npcraft:survival/respawn with entity @s data.home
