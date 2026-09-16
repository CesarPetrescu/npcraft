execute unless score @s np.owner = #actor np.tmp run return 0
$execute unless data entity @a[tag=npcraft.actor,limit=1] {UUID:$(owner_uuid)} run return 0
scoreboard players set #authorized np.tmp 1
function npcraft:commands/owned
