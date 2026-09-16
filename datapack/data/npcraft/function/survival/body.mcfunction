# Prime the native death timer while ALIVE; on lethal damage the cosmetic body
# expires on its next living-entity tick instead of retaining an unsavable DYING
# mannequin pose for twenty ticks. This does not grant health or invulnerability.
$data merge entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=$(id)},limit=1] {Invulnerable:0b,DeathTime:19s,drop_chances:{mainhand:0.0f,offhand:0.0f,head:0.0f,chest:0.0f,legs:0.0f,feet:0.0f},DeathLootTable:"minecraft:empty"}
